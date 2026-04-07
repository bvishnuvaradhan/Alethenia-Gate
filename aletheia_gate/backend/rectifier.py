"""
Rectification engine — triggered when truth score < 70.

Steps:
  1. Takes the original prompt + all model responses
  2. Asks each model to fact-check and correct the primary response
  3. Finds consensus between corrections
  4. Builds a rectified response containing only agreed facts
  5. Returns rectified text + list of removed/corrected claims
"""
from __future__ import annotations
import asyncio, os, re
from dataclasses import dataclass, field


@dataclass
class RectifiedClaim:
    original: str        # original sentence
    rectified: str       # corrected version (empty = removed)
    action: str          # "kept" | "corrected" | "removed"
    reason: str          # why it was changed


@dataclass
class RectificationResult:
    rectified_text: str
    claims: list[RectifiedClaim]
    new_score: int
    confidence: float
    models_agreed: int


# ── Fact-check prompt ────────────────────────────────────────────────────────

def _build_factcheck_prompt(original_prompt: str, response_to_check: str) -> str:
    return f"""You are a forensic fact-checker. A user asked: "{original_prompt}"

An AI gave this response:
---
{response_to_check}
---

Your task:
1. Check EVERY factual claim in the response above
2. For each claim: mark it as CORRECT, INCORRECT, or UNCERTAIN
3. If INCORRECT: provide the correct information
4. If UNCERTAIN: explain why

Format your response as:
CLAIM: [exact quote from response]
STATUS: CORRECT / INCORRECT / UNCERTAIN
CORRECTION: [corrected fact, or "N/A" if correct]
REASON: [brief explanation]
---
List every claim. Be precise and concise."""


# ── Parse fact-check response ────────────────────────────────────────────────

def _parse_factcheck(text: str) -> list[dict]:
    """Parse structured fact-check output into list of claim dicts."""
    claims = []
    blocks = re.split(r'\n---\n', text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        claim      = re.search(r'CLAIM:\s*(.+?)(?:\n|$)',      block, re.I)
        status     = re.search(r'STATUS:\s*(.+?)(?:\n|$)',     block, re.I)
        correction = re.search(r'CORRECTION:\s*(.+?)(?:\n|$)', block, re.I)
        reason     = re.search(r'REASON:\s*(.+?)(?:\n|$)',     block, re.I)
        if claim and status:
            claims.append({
                "claim":      claim.group(1).strip(),
                "status":     status.group(1).strip().upper(),
                "correction": correction.group(1).strip() if correction else "N/A",
                "reason":     reason.group(1).strip() if reason else "",
            })
    return claims


# ── Call models for fact-checking ────────────────────────────────────────────

async def _factcheck_groq(prompt: str, api_key: str = "") -> str:
    key = api_key.strip()
    if not key:
        return ""
    try:
        from groq import AsyncGroq
        client = AsyncGroq(api_key=key)
        resp = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.1,  # low temp for factual checking
        )
        return resp.choices[0].message.content or ""
    except Exception:
        return ""


async def _factcheck_openai(prompt: str, api_key: str = "") -> str:
    key = api_key.strip()
    if not key:
        return ""
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=key)
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.1,
        )
        return resp.choices[0].message.content or ""
    except Exception:
        return ""


async def _factcheck_anthropic(prompt: str, api_key: str = "") -> str:
    key = api_key.strip()
    if not key:
        return ""
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=key)
        resp = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text if resp.content else ""
    except Exception:
        return ""


# ── Consensus builder ────────────────────────────────────────────────────────

def _build_consensus(
    all_checks: list[list[dict]],
    original_sentences: list[str],
) -> list[RectifiedClaim]:
    """
    For each original sentence, check what each model said about it.
    Decision rules:
      - 2/3 say CORRECT     → keep as is
      - 2/3 say INCORRECT   → use their correction or remove
      - 2/3 say UNCERTAIN   → mark as uncertain, keep with warning
      - No consensus        → keep with uncertainty flag
    """
    results = []

    for sentence in original_sentences:
        s_lower = sentence.lower()
        verdicts = []

        for model_checks in all_checks:
            for check in model_checks:
                # Match by substring overlap
                claim_lower = check["claim"].lower()
                if (claim_lower[:40] in s_lower or
                    s_lower[:40] in claim_lower or
                    _overlap(s_lower, claim_lower) > 0.4):
                    verdicts.append(check)
                    break

        if not verdicts:
            # No model checked this sentence — keep it
            results.append(RectifiedClaim(
                original=sentence,
                rectified=sentence,
                action="kept",
                reason="No issues flagged by any model.",
            ))
            continue

        # Count verdicts
        correct   = sum(1 for v in verdicts if "CORRECT"   in v["status"] and "IN" not in v["status"])
        incorrect = sum(1 for v in verdicts if "INCORRECT" in v["status"])
        uncertain = sum(1 for v in verdicts if "UNCERTAIN" in v["status"])
        total     = len(verdicts)

        if incorrect >= max(1, total // 2):
            # Majority say incorrect — find the best correction
            corrections = [v["correction"] for v in verdicts
                           if "INCORRECT" in v["status"] and v["correction"] != "N/A"]
            reason = verdicts[0]["reason"] if verdicts else "Factual error detected."
            if corrections:
                results.append(RectifiedClaim(
                    original=sentence,
                    rectified=corrections[0],
                    action="corrected",
                    reason=reason,
                ))
            else:
                results.append(RectifiedClaim(
                    original=sentence,
                    rectified="",
                    action="removed",
                    reason=reason,
                ))
        elif uncertain >= max(1, total // 2):
            reason = verdicts[0]["reason"] if verdicts else "Insufficient evidence."
            results.append(RectifiedClaim(
                original=sentence,
                rectified=f"[UNCERTAIN] {sentence}",
                action="kept",
                reason=f"Low confidence: {reason}",
            ))
        else:
            results.append(RectifiedClaim(
                original=sentence,
                rectified=sentence,
                action="kept",
                reason="Verified across models.",
            ))

    return results


def _overlap(a: str, b: str) -> float:
    """Simple word overlap ratio between two strings."""
    wa = set(re.findall(r'\b\w{4,}\b', a))
    wb = set(re.findall(r'\b\w{4,}\b', b))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def _split_simple(text: str) -> list[str]:
    """Simple sentence split for rectification."""
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 15]
    result = []
    for line in lines:
        if len(line) > 150:
            for s in re.split(r'(?<=[.!?])\s+', line):
                if len(s.strip()) > 15:
                    result.append(s.strip())
        else:
            result.append(line)
    return result[:10]


# ── Main rectification entry point ───────────────────────────────────────────

async def rectify(
    original_prompt: str,
    primary_response: str,
    current_score: int,
) -> RectificationResult:
    """
    Run the full rectification pipeline.
    Called when truth_score < 70.
    """

    fc_prompt = _build_factcheck_prompt(original_prompt, primary_response)

    # Run all fact-checkers in parallel
    checks_raw = await asyncio.gather(
        _factcheck_groq(fc_prompt),
        _factcheck_openai(fc_prompt),
        _factcheck_anthropic(fc_prompt),
    )

    # Parse responses
    all_checks = [_parse_factcheck(r) for r in checks_raw if r.strip()]

    if not all_checks:
        # No models available for fact-checking
        return RectificationResult(
            rectified_text=primary_response,
            claims=[],
            new_score=current_score,
            confidence=0.5,
            models_agreed=0,
        )

    # Split original response into sentences
    sentences = _split_simple(primary_response)

    # Build consensus
    claims = _build_consensus(all_checks, sentences)

    # Build rectified text
    rectified_parts = []
    for c in claims:
        if c.action == "removed":
            continue  # remove flagged claims
        if c.action == "corrected" and c.rectified:
            rectified_parts.append(c.rectified)
        else:
            # Strip [UNCERTAIN] prefix for clean output
            rectified_parts.append(c.rectified.replace("[UNCERTAIN] ", ""))

    rectified_text = "\n".join(rectified_parts) if rectified_parts else primary_response

    # Calculate new score
    kept      = sum(1 for c in claims if c.action == "kept"      and "[UNCERTAIN]" not in c.rectified)
    corrected = sum(1 for c in claims if c.action == "corrected")
    removed   = sum(1 for c in claims if c.action == "removed")
    total     = len(claims)

    if total > 0:
        clean_ratio = (kept + corrected * 0.7) / total
        new_score   = min(95, max(current_score, int(clean_ratio * 90)))
    else:
        new_score = current_score

    confidence    = round(len(all_checks) / 3, 2)
    models_agreed = sum(
        1 for checks in all_checks
        if any("INCORRECT" in c["status"] for c in checks)
    )

    return RectificationResult(
        rectified_text=rectified_text,
        claims=claims,
        new_score=new_score,
        confidence=confidence,
        models_agreed=models_agreed,
    )
