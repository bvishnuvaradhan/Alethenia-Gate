"""
Advanced fact-checking with NER, semantic matching, and entity validation.
Uses sentence-transformers and spaCy for intelligent claim verification.
"""
from __future__ import annotations
import asyncio
import os
import re
from dataclasses import dataclass
from typing import Optional

# ─── Global Models (loaded once) ───────────────────────────────────────────
_MODEL = None
_NLP = None

def _load_models():
    """Load sentence transformer and spaCy models once globally."""
    global _MODEL, _NLP
    if _MODEL is None:
        try:
            os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
            os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
            try:
                from transformers.utils import logging as hf_logging
                hf_logging.set_verbosity_error()
                hf_logging.disable_progress_bar()
            except Exception:
                pass
            from sentence_transformers import SentenceTransformer
            # Default to local-only to avoid startup/network failures in offline environments.
            local_only = os.getenv("AG_HF_LOCAL_ONLY", "1") != "0"
            _MODEL = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=local_only)
        except Exception as e:
            print(f"[!] Sentence transformers unavailable: {e}")
            _MODEL = None

    if _NLP is None:
        try:
            import spacy
            _NLP = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"[!] spaCy model unavailable: {e}")
            _NLP = None


# ─── Data Structures ───────────────────────────────────────────────────────
@dataclass
class Entity:
    text: str
    label: str  # PERSON, GPE, ORG, etc.

@dataclass
class Triplet:
    subject: Optional[str]
    relation: Optional[str]
    obj: Optional[str]

@dataclass
class ClaimAnalysis:
    claim: str
    entities: list[Entity]
    triplet: Triplet
    normalized: str


# ─── 1. ENTITY EXTRACTION ──────────────────────────────────────────────────
def extract_entities(text: str) -> list[Entity]:
    """Extract named entities using spaCy."""
    if _NLP is None:
        return []

    doc = _NLP(text)
    return [
        Entity(text=ent.text, label=ent.label_)
        for ent in doc.ents
    ]


# ─── 2. RELATION EXTRACTION (S–P–O) ───────────────────────────────────────
def extract_triplet(text: str) -> Triplet:
    """Extract subject-predicate-object triplet using spaCy."""
    if _NLP is None:
        return Triplet(None, None, None)

    doc = _NLP(text)
    subject = None
    predicate = None
    obj = None

    for token in doc:
        if token.dep_ == "nsubj":
            subject = token.text
        elif token.dep_ == "ROOT":
            predicate = token.text
        elif token.dep_ in ("dobj", "attr", "pobj"):
            obj = token.text

    return Triplet(subject=subject, relation=predicate, obj=obj)


# ─── 3. SEMANTIC MATCHING ──────────────────────────────────────────────────
def semantic_score(a: str, b: str) -> float:
    """Compute cosine similarity between two texts (0-1)."""
    if _MODEL is None or not a or not b:
        return 0.0

    try:
        from sentence_transformers import util
        emb1 = _MODEL.encode(a, convert_to_tensor=True)
        emb2 = _MODEL.encode(b, convert_to_tensor=True)
        sim = util.cos_sim(emb1, emb2).item()
        return float(sim)
    except Exception as e:
        print(f"Semantic score error: {e}")
        return 0.0


# ─── 4. ENTITY-LEVEL VALIDATION ───────────────────────────────────────────
def entity_check(claim_obj: ClaimAnalysis, snippet: str) -> bool:
    """Check if claimed object appears in source snippet."""
    if not claim_obj.triplet.obj:
        return False

    obj_text = claim_obj.triplet.obj.lower()
    snippet_lower = snippet.lower()

    # Exact match or substring match
    return obj_text in snippet_lower or any(
        word in snippet_lower for word in obj_text.split()
    )


# ─── 5. CONTRADICTION DETECTION ───────────────────────────────────────────
def detect_conflict(claim_obj: ClaimAnalysis, snippet: str) -> bool:
    """Detect if claim contradicts the snippet."""
    if not claim_obj.triplet.obj:
        return False

    obj_text = claim_obj.triplet.obj.lower()
    snippet_lower = snippet.lower()

    # Check for explicit negations
    negations = ["not", "no ", "isn't", "aren't", "doesn't", "don't"]

    for neg in negations:
        if f"{neg} {obj_text}" in snippet_lower:
            return True

    # Object not found = potential contradiction
    if obj_text not in snippet_lower:
        return True

    return False


# ─── 6. CLAIM ANALYSIS ────────────────────────────────────────────────────
def analyze_claim(claim: str) -> ClaimAnalysis:
    """Full analysis of a claim."""
    entities = extract_entities(claim)
    triplet = extract_triplet(claim)
    normalized = claim.lower().strip()

    return ClaimAnalysis(
        claim=claim,
        entities=entities,
        triplet=triplet,
        normalized=normalized
    )


# ─── 7. SCORING ENGINE ────────────────────────────────────────────────────
WEIGHTS = {
    "Wikipedia": 0.4,
    "Wikidata": 0.35,
    "DuckDuckGo": 0.25,
}

def compute_score(claim_obj: ClaimAnalysis, sources: list[dict]) -> tuple[float, int]:
    """
    Compute verification score (0-1) and count conflicts.

    Args:
        claim_obj: Analyzed claim
        sources: List of source dicts with 'name', 'excerpt', 'confidence'

    Returns:
        (score, conflict_count)
    """
    if not sources:
        return 0.0, 0

    score = 0.0
    conflicts = 0
    total_weight = 0.0

    for source in sources:
        snippet = source.get("excerpt", "")
        source_name = source.get("name", "")
        base_confidence = source.get("confidence", 0.8)

        if not snippet:
            continue

        # Semantic similarity
        sim = semantic_score(claim_obj.claim, snippet)

        # Entity match bonus
        entity_match = entity_check(claim_obj, snippet)
        if entity_match:
            sim += 0.15

        # Conflict penalty
        if detect_conflict(claim_obj, snippet):
            conflicts += 1
            sim -= 0.25

        # Final score for this source
        source_score = sim * base_confidence

        # Weight by source type
        weight = WEIGHTS.get(source_name.split(":")[0], 0.2)
        score += source_score * weight
        total_weight += weight

    # Normalize by total weight
    if total_weight > 0:
        score = score / total_weight

    # Clamp to [0, 1]
    score = max(0.0, min(1.0, score))

    return score, conflicts


# ─── 8. CLASSIFICATION ────────────────────────────────────────────────────
def classify_verdict(score: float, conflicts: int) -> tuple[str, str]:
    """
    Classify claim as TRUE, PARTIAL, or HALLUCINATION.

    Returns: (verdict, emoji_icon)
    """
    if conflicts > 1:
        return "CONFLICT", "⚠️"

    if score > 0.75:
        return "VERIFIED", "✅"
    elif score > 0.4:
        return "PARTIAL", "⚡"
    else:
        return "UNVERIFIED", "❌"


# ─── 9. ERROR HIGHLIGHTING ───────────────────────────────────────────────
def highlight_errors(claim: str, correct_text: str) -> list[tuple[str, str]]:
    """
    Mark words as correct/wrong based on presence in source text.

    Returns: [(word, "correct"/"wrong"), ...]
    """
    words = claim.split()
    highlights = []
    correct_lower = correct_text.lower()

    for word in words:
        # Remove punctuation for matching
        word_clean = re.sub(r'[.,!?;:]', '', word).lower()

        if word_clean and word_clean in correct_lower:
            highlights.append((word, "correct"))
        else:
            highlights.append((word, "wrong"))

    return highlights


# ─── 10. FULL VERIFICATION PIPELINE ───────────────────────────────────────
async def verify_claims_advanced(
    ai_text: str,
    sources: list[dict]
) -> list[dict]:
    """
    Full verification pipeline for all claims in AI response.

    Args:
        ai_text: The AI-generated response
        sources: List of web sources [{name, excerpt, confidence, url}, ...]

    Returns:
        List of verification results with claims, verdicts, scores, highlights
    """
    _load_models()

    # Extract claims (simple sentence splitting)
    claims = re.split(r'(?<=[.!?])\s+', ai_text.strip())
    claims = [c.strip() for c in claims if c.strip() and len(c) > 10]

    results = []

    for claim in claims:
        # Analyze claim
        claim_obj = analyze_claim(claim)

        # Score against sources
        score, conflicts = compute_score(claim_obj, sources)

        # Get verdict
        verdict, icon = classify_verdict(score, conflicts)

        # Highlight errors
        source_text = " ".join([s.get("excerpt", "") for s in sources])
        highlights = highlight_errors(claim, source_text)

        results.append({
            "claim": claim,
            "verdict": verdict,
            "icon": icon,
            "score": round(score, 3),
            "conflicts": conflicts,
            "highlights": highlights,
            "entities": [{"text": e.text, "label": e.label} for e in claim_obj.entities],
            "triplet": {
                "subject": claim_obj.triplet.subject,
                "relation": claim_obj.triplet.relation,
                "object": claim_obj.triplet.obj
            }
        })

    return results


# Models are loaded lazily by verify_claims_advanced().
