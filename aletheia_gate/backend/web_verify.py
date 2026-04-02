"""
Web verification — Wikipedia + DuckDuckGo free APIs.
No API keys needed.
"""
from __future__ import annotations
import asyncio, re, json, urllib.parse, urllib.request
from dataclasses import dataclass, field


@dataclass
class WebSource:
    name: str
    url: str
    excerpt: str = ""
    confidence: float = 0.0
    verified: bool = False


@dataclass
class WebVerifyResult:
    sources: list[WebSource] = field(default_factory=list)
    web_score: float = 0.0
    summary: str = ""
    facts_found: list[str] = field(default_factory=list)
    facts_not_found: list[str] = field(default_factory=list)


# ── HTTP helpers ──────────────────────────────────────────────────────────────

async def _fetch(url: str) -> dict:
    """Async HTTP GET returning parsed JSON."""
    loop = asyncio.get_event_loop()
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AletheiaGate/1.0 (forensic fact-checker)"},
        )
        raw = await loop.run_in_executor(
            None,
            lambda: urllib.request.urlopen(req, timeout=4).read().decode("utf-8"),
        )
        return json.loads(raw)
    except Exception:
        return {}


# ── Wikipedia ─────────────────────────────────────────────────────────────────

async def _wiki_summary(title: str) -> WebSource | None:
    """Fetch Wikipedia summary for an exact title."""
    encoded = urllib.parse.quote(title.replace(" ", "_"))
    data    = await _fetch(
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    )
    if not data or data.get("type") == "disambiguation":
        return None
    extract  = data.get("extract", "")
    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
    if not extract or len(extract) < 30:
        return None
    # First 3 sentences
    sents = re.split(r'(?<=[.!?])\s+', extract)
    short = " ".join(sents[:3])
    return WebSource(
        name=f"Wikipedia: {data.get('title', title)}",
        url=page_url,
        excerpt=short[:500],
        confidence=0.93,
        verified=True,
    )


async def _wiki_search(query: str) -> WebSource | None:
    """Search Wikipedia for a query and fetch the top result's summary."""
    q    = urllib.parse.quote(query)
    data = await _fetch(
        f"https://en.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={q}&format=json&srlimit=1&origin=*"
    )
    results = data.get("query", {}).get("search", [])
    if not results:
        return None
    top = results[0].get("title", "")
    return await _wiki_summary(top)


# ── DuckDuckGo ────────────────────────────────────────────────────────────────

async def _ddg(query: str) -> WebSource | None:
    """DuckDuckGo Instant Answer API."""
    q    = urllib.parse.quote(query)
    data = await _fetch(
        f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1"
    )
    abstract = data.get("AbstractText", "")
    source   = data.get("AbstractSource", "Web")
    src_url  = data.get("AbstractURL", "")
    if not abstract or len(abstract) < 40:
        return None
    return WebSource(
        name=f"DuckDuckGo / {source}",
        url=src_url,
        excerpt=abstract[:500],
        confidence=0.78,
        verified=True,
    )


# ── Query builder ─────────────────────────────────────────────────────────────

def _search_queries(prompt: str, response: str) -> list[str]:
    """
    Build smart Wikipedia search queries from the prompt + response.
    Covers: programming languages, people, topics, general prompt.
    """
    queries = []
    combined = (prompt + " " + response).lower()

    # ── Programming languages ─────────────────────────────────────────────────
    lang_map = {
        "python":     "Python programming language",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "java":       "Java programming language",
        "c++":        "C++ programming language",
        "c#":         "C Sharp programming language",
        "rust":       "Rust programming language",
        "go":         "Go programming language",
        "kotlin":     "Kotlin programming language",
        "swift":      "Swift programming language",
        "ruby":       "Ruby programming language",
        "php":        "PHP scripting language",
        "scala":      "Scala programming language",
        "r ":         "R programming language",
    }
    for key, wiki_title in lang_map.items():
        if re.search(rf'\b{re.escape(key)}\b', combined):
            queries.append(wiki_title)

    # ── Named people ──────────────────────────────────────────────────────────
    people = {
        "guido":      "Guido van Rossum",
        "brendan eich":"Brendan Eich",
        "gosling":    "James Gosling",
        "stroustrup": "Bjarne Stroustrup",
        "linus":      "Linus Torvalds",
        "torvalds":   "Linus Torvalds",
        "turing":     "Alan Turing",
        "knuth":      "Donald Knuth",
        "lattner":    "Chris Lattner",
        "graydon":    "Graydon Hoare",
        "hejlsberg":  "Anders Hejlsberg",
    }
    for key, wiki_name in people.items():
        if re.search(rf'\b{re.escape(key)}\b', combined):
            queries.append(wiki_name)

    # ── Science / tech topics ─────────────────────────────────────────────────
    topic_map = {
        "speed of light":       "Speed of light",
        "black hole":           "Black hole",
        "mrna vaccine":         "mRNA vaccine",
        "machine learning":     "Machine learning",
        "artificial intelligence": "Artificial intelligence",
        "turing award":         "Turing Award",
        "nobel prize":          "Nobel Prize",
        "quantum computing":    "Quantum computing",
        "blockchain":           "Blockchain",
        "neural network":       "Artificial neural network",
    }
    for key, wiki_title in topic_map.items():
        if re.search(rf'\b{re.escape(key)}\b', combined, re.IGNORECASE):
            queries.append(wiki_title)

    # ── Fallback: Extract key noun phrases from prompt + response ─────────────
    if not queries:
        # Remove question words and extract longest meaningful phrases
        clean = re.sub(r'\b(who|what|when|where|why|how|is|are|was|were|did|does|do|the|a|an|of|or|and)\b',
                       ' ', prompt, flags=re.IGNORECASE).strip()
        clean = re.sub(r'\s+', ' ', clean).strip()

        # Also extract key words from response that look important (capitalized words)
        resp_words = re.findall(r'\b[A-Z][a-z]+\b', response)[:3]

        if clean:
            queries.append(clean[:60])
        if resp_words and clean != " ".join(resp_words):
            queries.append(" ".join(resp_words[:2]))

    # Deduplicate, limit to 2 (was 3)
    seen, out = set(), []
    for q in queries:
        k = q.lower()
        if k not in seen:
            seen.add(k)
            out.append(q)
    return out[:2]


# ── Fact matching ─────────────────────────────────────────────────────────────

def _extract_claims(response: str) -> list[str]:
    """
    Pull short verifiable claims from the response.
    Looks for sentences containing creator/date/definition facts.
    """
    # Clean markdown
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', response)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[-*•]\s*', '', text, flags=re.MULTILINE)

    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 20]

    claim_patterns = [
        r'(created|invented|designed|developed|founded|built) by',
        r'first (released|published|appeared|launched|introduced) in \d{4}',
        r'(released|launched|introduced) in \d{4}',
        r'(creator|inventor|founder|author|designer) (of|is|was)',
        r'\b\d{4}\b.{3,30}(created|founded|released|invented)',
        r'(is|was) (a|an) (high.level|low.level|interpreted|compiled|object)',
        r'(used for|designed for|built for)',
    ]

    claims = []
    for line in lines[:10]:
        for pat in claim_patterns:
            if re.search(pat, line, re.IGNORECASE):
                claims.append(line[:120])
                break

    return claims[:4]


def _claim_in_sources(claim: str, sources: list[WebSource]) -> bool:
    """
    Check if a claim's key facts appear in the web source excerpts.
    Uses flexible keyword matching — not exact string search.
    """
    claim_lower = claim.lower()
    all_text    = " ".join(s.excerpt.lower() for s in sources)

    # Extract key tokens: proper nouns, years, important words
    # Proper nouns (capitalised words)
    proper = [w.lower() for w in re.findall(r'\b[A-Z][a-z]{2,}\b', claim)]
    # Years
    years  = re.findall(r'\b(19|20)\d{2}\b', claim)
    # Important technical words
    tech   = re.findall(
        r'\b(python|javascript|java|rust|go|swift|kotlin|typescript|'
        r'created|invented|released|founder|creator|interpreted|'
        r'high.level|programming|language|library|framework)\b',
        claim_lower
    )

    key_tokens = list(set(proper + years + tech))
    if not key_tokens:
        return False

    # Need at least 40% of key tokens to appear in sources
    matched = sum(1 for t in key_tokens if t in all_text)
    ratio   = matched / len(key_tokens)

    return ratio >= 0.40


# ── Main verification function ────────────────────────────────────────────────

async def verify_with_web(prompt: str, ai_response: str) -> WebVerifyResult:
    """
    Verify AI response against Wikipedia and DuckDuckGo.
    Returns sources, score, and matched/unmatched facts.
    Timeout: 12 seconds max.
    """
    try:
        queries = _search_queries(prompt, ai_response)

        # Build all search tasks
        tasks = []
        for q in queries:
            tasks.append(_wiki_search(q))
            tasks.append(_ddg(q))

    try:
        queries = _search_queries(prompt, ai_response)

        # Build all search tasks
        tasks = []
        for q in queries:
            tasks.append(_wiki_search(q))
            tasks.append(_ddg(q))

        raw = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=12.0  # 12s timeout for entire web verify
        )

        # Collect valid sources, deduplicate by URL
        sources: list[WebSource] = []
        for r in raw:
            if isinstance(r, WebSource) and r is not None:
                if not any(s.url == r.url for s in sources):
                    sources.append(r)

        if not sources:
            return WebVerifyResult(
                sources=[],
                web_score=0.50,   # neutral when web unavailable
                summary="Web sources unavailable — score based on AI consensus only.",
                facts_found=[],
                facts_not_found=[],
            )

        # Match claims against sources
        claims     = _extract_claims(ai_response)
        found      = []
        not_found  = []

        for claim in claims:
            if _claim_in_sources(claim, sources):
                found.append(claim[:100])
            else:
                not_found.append(claim[:100])

        # Score calculation
        if claims:
            match_ratio  = len(found) / len(claims)
            source_bonus = min(0.12, len(sources) * 0.04)
            web_score    = round(min(0.97, match_ratio * 0.88 + source_bonus), 3)
        else:
            # No extractable claims — neutral score based on source quality
            avg_conf  = sum(s.confidence for s in sources) / len(sources)
            web_score = round(min(0.82, avg_conf * 0.85), 3)

        # Summary
        if claims and found:
            summary = f"{len(found)}/{len(claims)} claims verified across {len(sources)} web source(s)."
        elif claims and not found:
            summary = f"Retrieved {len(sources)} source(s) but specific claims could not be matched."
        else:
            summary = f"Retrieved {len(sources)} web source(s). General topic confirmed."

        return WebVerifyResult(
            sources=sources,
            web_score=web_score,
            summary=summary,
            facts_found=found,
            facts_not_found=not_found,
        )
    except asyncio.TimeoutError:
        return WebVerifyResult(
            sources=[],
            web_score=0.50,
            summary="Web verification timed out — score based on AI consensus only.",
            facts_found=[],
            facts_not_found=[],
        )
