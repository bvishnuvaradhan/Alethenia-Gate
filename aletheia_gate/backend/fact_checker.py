"""
Dedicated fact-checker — finds real errors in AI responses.

_ALWAYS_CORRECT: these phrases are scientifically correct and must
never be flagged as errors regardless of what the AI fact-checker says.
"""
from __future__ import annotations
import asyncio, os, re
from dataclasses import dataclass, field


@dataclass
class FactError:
    claim: str
    correction: str
    confidence: float
    source: str


@dataclass
class FactCheckResult:
    errors_found: list[FactError] = field(default_factory=list)
    checked: bool = False
    checker_used: str = ""
    penalty: float = 0.0


# ── Scientifically correct facts — NEVER flag these ───────────────────────────
_ALWAYS_CORRECT = [
    # Earth rotation — west to east is CORRECT
    "earth rotates from west to east",
    "earth rotates west to east",
    "earth spins from west to east",
    "earth spinning from west to east",
    "rotating from west to east",
    "rotation from west to east",
    "rotates from west to east",
    "spinning from west to east",
    "earth's rotation from west to east",
    # Sun directions (result of west-to-east rotation)
    "sun rises in the east",
    "sun rises from the east",
    "sun sets in the west",
    "sun sets to the west",
    "sun appears to move westward",
    "appears to set in the west",
    # Basic physics
    "water boils at 100",
    "water freezes at 0",
    "speed of light is 299",
    "pi is approximately 3.14",
    "e = mc",
    # Biology
    "humans have 46 chromosomes",
    "dna has four bases",
    "heart has four chambers",
    # Astronomy
    "earth orbits the sun",
    "moon orbits the earth",
    "8 planets in the solar system",
]

def _is_protected(claim: str) -> bool:
    c = claim.lower()
    return any(fact in c for fact in _ALWAYS_CORRECT)


_PROMPT = """You are a strict fact-checker. Your job is to find ONLY clear, undeniable factual errors.

CRITICAL RULES:
1. "The Earth rotates from west to east" is 100% CORRECT — never flag this
2. "The sun sets in the west" is CORRECT — never flag this
3. "The sun rises in the east" is CORRECT — never flag this
4. Only flag things you are absolutely certain (95%+) are wrong
5. Do NOT flag opinions, estimates, or things you are uncertain about
6. Do NOT flag correct scientific facts

For each real error output EXACTLY this format:
ERROR: [exact wrong text from the passage]
CORRECT: [the true fact]
CONFIDENCE: HIGH

If no clear errors exist, output only: NO_ERRORS

Passage to check:
{text}"""


async def _check_groq(text: str) -> tuple[str, str]:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        return "", ""
    try:
        from groq import AsyncGroq
        resp = await AsyncGroq(api_key=key).chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": _PROMPT.format(text=text[:2000])}],
            max_tokens=400, temperature=0.0,  # 0 temp = most deterministic
        )
        return resp.choices[0].message.content or "", "Groq/Llama-3.3"
    except Exception:
        return "", ""


async def _check_openai(text: str) -> tuple[str, str]:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return "", ""
    try:
        from openai import AsyncOpenAI
        resp = await AsyncOpenAI(api_key=key).chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": _PROMPT.format(text=text[:2000])}],
            max_tokens=400, temperature=0.0,
        )
        return resp.choices[0].message.content or "", "OpenAI/GPT-4o-mini"
    except Exception:
        return "", ""


def _parse(raw: str) -> list[FactError]:
    if not raw or "NO_ERRORS" in raw.upper():
        return []
    errors = []
    blocks = re.split(r'(?:^|\n)ERROR:', raw)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m_claim   = re.match(r'^(.+?)(?:\nCORRECT:|$)', block, re.DOTALL)
        m_correct = re.search(r'CORRECT:\s*(.+?)(?:\nCONFIDENCE:|$)', block, re.DOTALL)
        m_conf    = re.search(r'CONFIDENCE:\s*(HIGH|MEDIUM|LOW)', block, re.IGNORECASE)
        if not m_claim:
            continue
        claim      = m_claim.group(1).strip()[:200]
        correction = m_correct.group(1).strip()[:200] if m_correct else "See verified sources"
        conf_str   = (m_conf.group(1).upper() if m_conf else "MEDIUM")
        conf_val   = {"HIGH": 0.90, "MEDIUM": 0.65, "LOW": 0.40}.get(conf_str, 0.65)

        # Skip protected correct facts
        if _is_protected(claim):
            continue
        # Skip if the "correction" itself is a known correct fact being mislabeled
        if _is_protected(correction):
            continue

        if len(claim) > 10:
            errors.append(FactError(
                claim=claim, correction=correction,
                confidence=conf_val, source="AI fact-checker"
            ))
    return errors[:5]


def _penalty(errors: list[FactError]) -> float:
    if not errors:
        return 0.0
    p = sum(
        0.15 if e.confidence >= 0.85 else
        0.08 if e.confidence >= 0.55 else 0.03
        for e in errors
    )
    return min(0.45, p)


async def run_fact_check(primary_response: str) -> FactCheckResult:
    if not primary_response or len(primary_response) < 50:
        return FactCheckResult()

    # Only use Groq (OpenAI not configured)
    groq_r, _ = await asyncio.gather(
        _check_groq(primary_response),
        asyncio.sleep(0),  # Skip OpenAI wait
    )

    raw, model = "", ""
    if groq_r[0]:
        raw, model = groq_r
    else:
        return FactCheckResult(checked=False)

    errors = _parse(raw)
    return FactCheckResult(
        errors_found=errors,
        checked=True,
        checker_used=model,
        penalty=_penalty(errors),
    )
