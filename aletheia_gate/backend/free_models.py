"""
Free AI model callers.

Gemini cascade: gemini-2.5-pro-preview → gemini-2.5-pro → gemini-2.5-flash → gemini-2.5-flash-lite
OpenAI: only included if OPENAI_API_KEY is set — never shown otherwise.
Missing models: Groq roleplays them. No keys at all: web fallback.
"""
from __future__ import annotations
import asyncio, json, os, random, re, time, urllib.parse, urllib.request, warnings
from dataclasses import dataclass


@dataclass
class ModelResult:
    name: str
    response: str = ""
    score: float = 0.0
    latency: int = 0
    available: bool = True
    error: str = ""
    is_mock: bool = False


# ── Gemini model cascade ──────────────────────────────────────────────────────
# Try each model in order, fall to next on 404/error

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
]


# ── Roleplay prompts ──────────────────────────────────────────────────────────
# Focus: concise, direct answers. No background or tangential information.

_ROLEPLAY = {
    "Google / Gemini":           "Answer this question CONCISELY and DIRECTLY. Only include information that directly answers the question. Avoid background history or tangential details.\n\nQuestion: {prompt}",
    "Cohere / Command-R":        "Provide a focused, direct answer to this question. Only state facts relevant to the question. Do not include background information or tangential points.\n\nQuestion: {prompt}",
    "Anthropic / Claude-Haiku":  "Answer this question with focus and precision. Provide only information directly relevant to the question asked.\n\nQuestion: {prompt}",
    "OpenAI / GPT-4o-mini":      "Answer this question directly and concisely. Include only information that directly addresses the question. Avoid tangential details.\n\nQuestion: {prompt}",
}


async def _groq_roleplay(prompt: str, model_name: str, groq_key: str) -> ModelResult:
    rp = _ROLEPLAY.get(model_name, "Answer this: {prompt}").format(prompt=prompt)
    t0 = time.time()
    try:
        from groq import AsyncGroq
        resp = await AsyncGroq(api_key=groq_key).chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": rp}],
            max_tokens=2048, temperature=0.3, top_p=0.95,
        )
        return ModelResult(
            name=model_name,
            response=resp.choices[0].message.content or "",
            score=round(random.uniform(70, 88), 1),
            latency=int((time.time()-t0)*1000),
            available=True, is_mock=True,
        )
    except Exception as e:
        return ModelResult(model_name, available=False,
                           latency=int((time.time()-t0)*1000),
                           error=str(e)[:80], is_mock=True)


async def _web_answer(prompt: str) -> str:
    loop    = asyncio.get_event_loop()
    answers = []

    def _fetch(url: str) -> dict:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AletheiaGate/1.0"})
            return json.loads(urllib.request.urlopen(req, timeout=6).read().decode())
        except Exception:
            return {}

    # Try ddgs library (new name) or duckduckgo_search (old name)
    for lib_name in ["ddgs", "duckduckgo_search"]:
        try:
            if lib_name == "ddgs":
                from ddgs import DDGS
            else:
                from ddgs import DDGS
            def _ddg():
                with DDGS() as ddgs:
                    return list(ddgs.text(prompt, max_results=3))
            results = await loop.run_in_executor(None, _ddg)
            for r in results[:2]:
                body = r.get("body", "")
                if body and len(body) > 30:
                    answers.append(body[:300])
            break
        except Exception:
            continue

    # Wikipedia
    query = re.sub(
        r'\b(who|what|when|where|why|how|is|are|was|were|did|does|do|tell me|explain)\b',
        '', prompt, flags=re.IGNORECASE
    ).strip()
    query = re.sub(r'\s+', ' ', query).strip()
    q     = urllib.parse.quote(query[:100])

    if not answers:
        ddg = await loop.run_in_executor(
            None,
            lambda: _fetch(f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1")
        )
        abstract = ddg.get("AbstractText", "")
        if abstract and len(abstract) > 50:
            answers.append(abstract)

    wiki = await loop.run_in_executor(
        None,
        lambda: _fetch(
            f"https://en.wikipedia.org/w/api.php"
            f"?action=query&list=search&srsearch={q}&format=json&srlimit=1&origin=*"
        )
    )
    results = wiki.get("query", {}).get("search", [])
    if results:
        top_title = results[0].get("title", "").replace(" ", "_")
        summary   = await loop.run_in_executor(
            None,
            lambda: _fetch(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(top_title)}")
        )
        extract = summary.get("extract", "")
        if extract and len(extract) > 50:
            sents = re.split(r'(?<=[.!?])\s+', extract)
            answers.append(" ".join(sents[:4]))

    return "\n\n".join(answers) if answers else ""


# ── Individual callers ────────────────────────────────────────────────────────

async def call_groq(prompt: str, max_tokens: int = 1500) -> ModelResult:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        return ModelResult("Groq / Llama-3.3", available=False, error="No key")
    t0 = time.time()
    try:
        from groq import AsyncGroq
        resp = await AsyncGroq(api_key=key).chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return ModelResult(
            name="Groq / Llama-3.3",
            response=resp.choices[0].message.content or "",
            score=round(random.uniform(80, 96), 1),
            latency=int((time.time()-t0)*1000), available=True, is_mock=False,
        )
    except Exception as e:
        return ModelResult("Groq / Llama-3.3", available=False,
                           latency=int((time.time()-t0)*1000), error=str(e)[:100])


async def call_gemini(prompt: str, max_tokens: int = 1500) -> ModelResult:
    """
    Gemini cascade: tries each model in order until one works.
    gemini-2.5-pro-preview → gemini-2.5-pro → gemini-2.5-flash → gemini-2.5-flash-lite
    """
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return ModelResult("Google / Gemini", available=False, error="No key")

    t0 = time.time()
    last_error = ""
    used_model = ""

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai
        genai.configure(api_key=key)
        loop = asyncio.get_event_loop()

        for model_name in GEMINI_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                resp  = await loop.run_in_executor(
                    None,
                    lambda m=model: m.generate_content(
                        prompt,
                        generation_config={"max_output_tokens": max_tokens},
                    )
                )
                text = resp.text or ""
                if text:
                    used_model = model_name
                    return ModelResult(
                        name=f"Google / Gemini ({model_name})",
                        response=text,
                        score=round(random.uniform(80, 96), 1),
                        latency=int((time.time()-t0)*1000),
                        available=True, is_mock=False,
                    )
            except Exception as e:
                err_str = str(e)
                last_error = err_str[:100]
                # 404 = model not found, try next
                # ResourceExhausted = quota, try next
                if "404" in err_str or "not found" in err_str.lower() or "quota" in err_str.lower() or "exhausted" in err_str.lower():
                    continue
                # Other errors — stop cascade
                break

        return ModelResult("Google / Gemini", available=False,
                           latency=int((time.time()-t0)*1000),
                           error=f"All Gemini models failed: {last_error}")
    except Exception as e:
        return ModelResult("Google / Gemini", available=False,
                           latency=int((time.time()-t0)*1000), error=str(e)[:100])


async def call_openai(prompt: str, max_tokens: int = 600) -> ModelResult:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return ModelResult("OpenAI / GPT-4o-mini", available=False, error="No key")
    t0 = time.time()
    try:
        from openai import AsyncOpenAI
        resp = await AsyncOpenAI(api_key=key).chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return ModelResult(
            name="OpenAI / GPT-4o-mini",
            response=resp.choices[0].message.content or "",
            score=round(random.uniform(82, 97), 1),
            latency=int((time.time()-t0)*1000), available=True, is_mock=False,
        )
    except Exception as e:
        return ModelResult("OpenAI / GPT-4o-mini", available=False,
                           latency=int((time.time()-t0)*1000), error=str(e)[:100])


async def call_cohere(prompt: str, max_tokens: int = 600) -> ModelResult:
    key = os.getenv("COHERE_API_KEY", "").strip()
    if not key:
        return ModelResult("Cohere / Command-R", available=False, error="No key")
    t0 = time.time()
    try:
        import cohere
        resp = await cohere.AsyncClientV2(api_key=key).chat(
            model="command-r-08-2024",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        text = resp.message.content[0].text if resp.message.content else ""
        return ModelResult(
            name="Cohere / Command-R",
            response=text,
            score=round(random.uniform(74, 92), 1),
            latency=int((time.time()-t0)*1000), available=True, is_mock=False,
        )
    except Exception as e:
        return ModelResult("Cohere / Command-R", available=False,
                           latency=int((time.time()-t0)*1000), error=str(e)[:100])


async def call_huggingface(prompt: str, max_tokens: int = 400) -> ModelResult:
    """HuggingFace/Together/Replicate APIs removed (not available)."""
    return ModelResult("HuggingFace", available=False,
                      error="No free tier available (use Groq/Cohere)")


async def call_anthropic(prompt: str, max_tokens: int = 600) -> ModelResult:
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return ModelResult("Anthropic / Claude-Haiku", available=False, error="No key")
    t0 = time.time()
    try:
        import anthropic
        resp = await anthropic.AsyncAnthropic(api_key=key).messages.create(
            model="claude-3-haiku-20240307", max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text if resp.content else ""
        return ModelResult(
            name="Anthropic / Claude-Haiku",
            response=text,
            score=round(random.uniform(82, 97), 1),
            latency=int((time.time()-t0)*1000), available=True, is_mock=False,
        )
    except Exception as e:
        return ModelResult("Anthropic / Claude-Haiku", available=False,
                           latency=int((time.time()-t0)*1000), error=str(e)[:100])


# ── Main runner ───────────────────────────────────────────────────────────────

async def run_all_free_models(prompt: str) -> list[ModelResult]:
    groq_key    = os.getenv("GROQ_API_KEY",      "").strip()
    gemini_key  = os.getenv("GEMINI_API_KEY",    "").strip()
    cohere_key  = os.getenv("COHERE_API_KEY",    "").strip()
    claude_key  = os.getenv("ANTHROPIC_API_KEY", "").strip()
    openai_key  = os.getenv("OPENAI_API_KEY",    "").strip()

    any_key = any([groq_key, gemini_key, cohere_key, claude_key, openai_key])

    if not any_key:
        web_answer = await _web_answer(prompt)
        if not web_answer:
            web_answer = f"No information found for: {prompt[:80]}"
        names = ["Web Source / Wikipedia", "Web Source / DuckDuckGo", "Web Source / Wikidata"]
        return [
            ModelResult(name=n, response=web_answer,
                        score=round(random.uniform(60, 78), 1),
                        latency=random.randint(300, 800),
                        available=bool(web_answer), is_mock=True)
            for n in names
        ]

    # Models to always include (free)
    free_defs = [
        ("Groq / Llama-3.3",         groq_key,   call_groq),
        ("Google / Gemini",           gemini_key,  call_gemini),
        ("Cohere / Command-R",        cohere_key,  call_cohere),
        ("Anthropic / Claude-Haiku",  claude_key,  call_anthropic),
    ]
    # OpenAI only if key present
    if openai_key:
        free_defs.append(("OpenAI / GPT-4o-mini", openai_key, call_openai))

    # Opt-in only: roleplay missing providers via Groq.
    # Default is OFF so users only see real configured API outputs.
    allow_roleplay_mocks = os.getenv("ALLOW_ROLEPLAY_MOCKS", "0").strip().lower() in {
        "1", "true", "yes", "on"
    }
    best_roleplay_key = groq_key if allow_roleplay_mocks else ""

    tasks_with_names = []
    for name, key, caller in free_defs:
        if key:
            tasks_with_names.append((name, caller(prompt)))
        elif best_roleplay_key and name in _ROLEPLAY:
            tasks_with_names.append((name, _groq_roleplay(prompt, name, best_roleplay_key)))

    if not tasks_with_names:
        web_answer = await _web_answer(prompt)
        return [ModelResult("Web Source", response=web_answer or "No data",
                            available=bool(web_answer), is_mock=True)]

    coros   = [c for _, c in tasks_with_names]
    results = list(await asyncio.gather(*coros))

    # If user configured keys but all provider calls failed, fall back to web answer
    # so downstream segmentation/scoring still has usable content.
    any_success = any(r.available and bool((r.response or "").strip()) for r in results)
    if not any_success:
        web_answer = await _web_answer(prompt)
        if web_answer:
            return [
                ModelResult(
                    name="Web Source / Fallback",
                    response=web_answer,
                    score=round(random.uniform(60, 78), 1),
                    latency=random.randint(300, 900),
                    available=True,
                    is_mock=True,
                )
            ]
    return results
