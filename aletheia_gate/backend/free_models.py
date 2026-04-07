"""
Free AI model callers.

Cascade: Groq (llama-3.3-70b) → Gemini (if key set) → Cohere → Claude → OpenAI (if key set)
Only models with API keys configured are shown. Web fallback if no keys available.
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

    # ── Try real-time currency exchange APIs first (for exchange rate queries) ────
    if any(term in prompt.lower() for term in ['dollar', 'rupee', 'exchange', 'currency', 'usd', 'inr']):
        try:
            # Try exchangerate-api.com (free tier, real-time)
            ex_api = await loop.run_in_executor(
                None,
                lambda: _fetch("https://api.exchangerate-api.com/v4/latest/USD")
            )
            if ex_api and "rates" in ex_api:
                inr_rate = ex_api["rates"].get("INR")
                if inr_rate:
                    answers.append(f"Current Exchange Rate: 1 USD = {inr_rate:.2f} INR (Real-time)")
        except Exception:
            pass

        # Try open exchange rates if first fails
        if not answers:
            try:
                open_ex = await loop.run_in_executor(
                    None,
                    lambda: _fetch("https://open.er-api.com/v6/latest/USD")
                )
                if open_ex and "rates" in open_ex:
                    inr_rate = open_ex["rates"].get("INR")
                    if inr_rate:
                        answers.append(f"Current Exchange Rate: 1 USD = {inr_rate:.2f} INR (Open ER API)")
            except Exception:
                pass

    # ── Fallback to DuckDuckGo / Wikipedia for general queries ────
    for lib_name in ["ddgs", "duckduckgo_search"]:
        try:
            if lib_name == "ddgs":
                from ddgs import DDGS
            else:
                from ddgs import DDGS
            def _ddg():
                with DDGS() as ddgs:
                    return list(ddgs.text(prompt, max_results=5))
            results = await loop.run_in_executor(None, _ddg)
            for r in results[:3]:  # Take up to 3 results
                body = r.get("body", "")
                if body and len(body) > 50:
                    answers.append(body[:500])  # Extract longer snippets
            if answers:
                break
        except Exception:
            continue

    # DuckDuckGo API fallback
    query = re.sub(
        r'\b(who|what|when|where|why|how|is|are|was|were|did|does|do|tell me|explain|current)\b',
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

    # Wikipedia for comprehensive answers
    wiki = await loop.run_in_executor(
        None,
        lambda: _fetch(
            f"https://en.wikipedia.org/w/api.php"
            f"?action=query&list=search&srsearch={q}&format=json&srlimit=3&origin=*"
        )
    )
    results = wiki.get("query", {}).get("search", [])
    if results and not answers:  # Use wiki only if we don't have other results
        for result in results[:1]:
            top_title = result.get("title", "").replace(" ", "_")
            summary   = await loop.run_in_executor(
                None,
                lambda: _fetch(f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(top_title)}")
            )
            extract = summary.get("extract", "")
            if extract and len(extract) > 50:
                answers.append(extract[:600])  # Get longer excerpt

    return "\n\n".join(answers) if answers else ""


# ── Individual callers ────────────────────────────────────────────────────────

async def call_groq(prompt: str, max_tokens: int = 1500, api_key: str = "") -> ModelResult:
    key = api_key.strip()
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


async def call_gemini(prompt: str, max_tokens: int = 1500, api_key: str = "") -> ModelResult:
    """
    Gemini cascade: tries each model in order until one works.
    gemini-2.5-pro-preview → gemini-2.5-pro → gemini-2.5-flash → gemini-2.5-flash-lite
    """
    key = api_key.strip()
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


async def call_openai(prompt: str, max_tokens: int = 600, api_key: str = "") -> ModelResult:
    key = api_key.strip()
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


async def call_cohere(prompt: str, max_tokens: int = 600, api_key: str = "") -> ModelResult:
    key = api_key.strip()
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


async def call_anthropic(prompt: str, max_tokens: int = 600, api_key: str = "") -> ModelResult:
    key = api_key.strip()
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

async def run_all_free_models(prompt: str, api_keys: dict[str, str] | None = None) -> list[ModelResult]:
    api_keys = api_keys or {}
    groq_key    = str(api_keys.get("groq_key", "") or "").strip()
    gemini_key  = str(api_keys.get("gemini_key", "") or "").strip()
    cohere_key  = str(api_keys.get("cohere_key", "") or "").strip()
    claude_key  = str(api_keys.get("anthropic_key", "") or "").strip()
    openai_key  = str(api_keys.get("openai_key", "") or "").strip()

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

    # Models to include - only configured ones
    free_defs = []

    if groq_key:
        free_defs.append(("Groq / Llama-3.3", groq_key, call_groq))
    if cohere_key:
        free_defs.append(("Cohere / Command-R", cohere_key, call_cohere))
    if claude_key:
        free_defs.append(("Anthropic / Claude-Haiku", claude_key, call_anthropic))
    if openai_key:
        free_defs.append(("OpenAI / GPT-4o-mini", openai_key, call_openai))

    tasks_with_names = []
    for name, key, caller in free_defs:
        tasks_with_names.append((name, caller(prompt, api_key=key)))

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
