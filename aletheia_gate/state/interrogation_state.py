"""Interrogation state — streaming + AI consensus + web verify + fact check."""
from __future__ import annotations
import reflex as rx
import time, asyncio, re
from .base import State, ModelStat, SegmentItem, AuditEntry, FactErrorItem, WebSourceItem
from ..backend.truth_engine import run_truth_engine, stream_primary_response, _is_segment_relevant
from ..backend.fact_checker import run_fact_check
from ..backend.vault_db import save_audit
from ..backend.free_sources import normalize_text, get_styled_claim
from ..backend.safety_wrapper import safe_execute, is_valid_prompt, get_cached_result, cache_result


def _filter_stream_for_relevance(full_response: str, prompt: str) -> str:
    """Filter streamed response to show only relevant sentences/paragraphs."""
    if not full_response or not prompt:
        return full_response

    # Remove citation/metadata lines first (Image source, Current topic, etc.)
    lines = [l for l in full_response.split('\n')
             if not re.search(r'image\s+source|author:|license:|current\s+topic|letsdiskuss', l, re.IGNORECASE)]
    full_response = '\n'.join(lines)

    # Don't over-filter - keep the full response as-is to avoid cutting off mid-sentence
    # The segmentation phase will handle relevance filtering
    return full_response.strip() if full_response.strip() else ""


class IntState(State):
    prompt: str = ""
    stream: str = ""
    streaming: bool = False
    running: bool = False
    audit_log: list[AuditEntry] = []
    styled_claim: list[dict] = []  # 🎨 For UI highlighting
    wrong_words: list[str] = []   # Words to highlight as wrong

    def go_interrogate(self):
        """Navigate to interrogation — clears state efficiently."""
        self.active_page = "interrogate"
        self.err_msg = ""
        # Batch clear all fields at once to avoid cascading re-renders
        self.prompt = ""
        self.stream = ""
        self.segments = []
        self.models = []
        self.truth_score = 0
        self.web_sources = 0
        self.web_score = 0.0
        self.web_summary = ""
        self.facts_verified = []
        self.facts_unverified = []
        self.fact_errors = []
        self.fact_check_done = False
        self.fact_penalty = 0.0
        self.status_msg = ""
        self.custody_id = ""
        self.latency_ms = 0
        self.web_source_names = []
        self.web_source_urls = []
        self.styled_claim = []  # 🎨 For UI highlighting
        self.wrong_words = []   # Words to highlight as wrong
        return rx.redirect("/interrogate")

    def set_prompt(self, v: str): self.prompt = v

    def _apply_result(self, result_tuple: tuple, prompt: str):
        """Apply truth engine and fact check results to state."""
        r, fc = result_tuple
        penalised_score = max(10, int(r.truth_score * (1.0 - fc.penalty)))

        # Store all results
        self.truth_score       = penalised_score
        self.consensus         = r.consensus_score
        self.semantic          = r.semantic_similarity
        self.alignment         = r.source_alignment
        self.custody_id        = r.chain_of_custody_id
        self.latency_ms        = r.latency_total
        self.models            = [
            ModelStat(name=m.name, response=m.response or "", score=round(m.score,1), latency=m.latency,
                      available=m.available, error=m.error or "",
                      is_mock=getattr(m, 'is_mock', False))
            for m in r.models
        ]
        self.segments          = [
            SegmentItem(text=s.text, status=s.status,
                        reason=s.reason or "", confidence=round(s.confidence, 2),
                        explanation=s.explanation or "", failed_entities=s.failed_entities or [])
            for s in r.segments
        ]
        self.web_sources       = r.web_sources
        self.web_score         = r.web_score
        self.web_summary       = r.web_summary
        self.facts_verified    = r.facts_verified
        self.facts_unverified  = r.facts_unverified
        self.web_source_names  = r.web_source_names if hasattr(r, 'web_source_names') else []
        self.web_source_urls   = r.web_source_urls if hasattr(r, 'web_source_urls') else []
        self.fact_errors       = [
            FactErrorItem(claim=e.claim, correction=e.correction,
                          confidence=round(e.confidence, 2), source=e.source)
            for e in fc.errors_found
        ]
        self.fact_checker_used = fc.checker_used or "Groq"
        self.fact_check_done = fc.checked
        self.fact_penalty = round(fc.penalty, 2)

        # 🎨 Generate styled claims for UI highlighting
        # Extract wrong words from unverified facts (first unverified claim)
        self.wrong_words = []
        if self.facts_unverified:
            first_unverified = self.facts_unverified[0]
            # Extract keywords from unverified claim for highlighting
            words = re.findall(r'\b\w+\b', first_unverified)
            # Highlight 2-3 most important looking words (longer words, nouns)
            long_words = [w for w in words if len(w) > 4 and w.lower() not in
                         {'about', 'which', 'where', 'their', 'would', 'could', 'should'}]
            self.wrong_words = long_words[:3]

        # Apply styling to stream
        if self.stream and self.wrong_words:
            self.styled_claim = get_styled_claim(self.stream, self.wrong_words)

    async def submit(self):
        # ── PREVENT DUPLICATE CLICKS ──────────────────────────────────────
        if not self.prompt.strip() or self.running:
            return

        # ── VALIDATE PROMPT ───────────────────────────────────────────────
        valid, err = is_valid_prompt(self.prompt)
        if not valid:
            self.err_msg = err
            return

        # ── CHECK CACHE (optional speedup) ────────────────────────────────
        cached = get_cached_result(self.prompt)
        if cached:
            self.status_msg = "Loading cached result..."
            yield
            # Use cached data
            self._apply_result(cached, self.prompt)
            self.status_msg = ""
            yield
            return

        # ── INITIALIZE ────────────────────────────────────────────────────
        self.running = True
        self.streaming = True
        self.stream = ""
        self.segments = []
        self.models = []
        self.truth_score = 0
        self.err_msg = ""
        self.web_sources = 0
        self.web_score = 0.0
        self.web_summary = ""
        self.facts_verified = []
        self.facts_unverified = []
        self.web_source_names = []
        self.web_source_urls = []
        self.fact_errors = []
        self.fact_checker_used = ""
        self.fact_check_done = False
        self.fact_penalty = 0.0
        self.status_msg = "🔍 Analyzing prompt..."
        p = self.prompt
        yield

        # ── STEP 1: STREAM PRIMARY RESPONSE ───────────────────────────────
        full = ""
        try:
            self.status_msg = "Routing to primary model..."
            yield
            async for tok in stream_primary_response(p):
                full += tok
                self.stream = full
                yield
        except Exception as ex:
            self.err_msg = f"⚠️ Stream error: {str(ex)[:80]}"
            self.streaming = False
            self.running = False
            yield
            return

        # ── STEP 1B: FILTER RESPONSE ──────────────────────────────────────
        filtered = _filter_stream_for_relevance(full, p)
        self.stream = filtered
        self.streaming = False
        yield

        # ── STEP 2: RUN CONSENSUS ENGINE (WITH TIMEOUT) ───────────────────
        self.status_msg = "🤖 Building consensus..."
        yield

        # Allow more time for multi-source verification and first-run model warmup.
        result = await safe_execute(
            run_truth_engine(p),
            timeout_sec=45,
            operation_name="Consensus engine"
        )

        if not result["success"]:
            self.err_msg = result["error"]
            self.running = False
            self.status_msg = ""
            yield
            return

        r = result["result"]

        # ── STEP 3: RUN FACT CHECK (WITH TIMEOUT) ─────────────────────────
        self.status_msg = "✓ Fact checking response..."
        yield

        fc_result = await safe_execute(
            run_fact_check(filtered),
            timeout_sec=12,
            operation_name="Fact checker"
        )

        if fc_result["success"]:
            fc = fc_result["result"]
        else:
            self.err_msg = fc_result["error"]
            self.running = False
            self.status_msg = ""
            yield
            return

        # ── STEP 4: APPLY RESULTS & CACHE ──────────────────────────────────
        self._apply_result((r, fc), p)
        cache_result(p, (r, fc))
        yield

        # ── STEP 5: SEAL TO VAULT ─────────────────────────────────────────
        self.status_msg = "🔐 Sealing to vault..."
        yield

        penalised_score = max(10, int(r.truth_score * (1.0 - fc.penalty)))
        await save_audit({
            "prompt": p,
            "truth_score": penalised_score,
            "consensus_score": r.consensus_score,
            "chain_of_custody_id": r.chain_of_custody_id,
            "created_at": time.time(),
            "web_sources": r.web_sources,
            "web_score": r.web_score,
            "errors_found": len(fc.errors_found),
        })
        self.audit_log = [
            AuditEntry(prompt=p[:80], truth_score=penalised_score,
                       custody_id=r.chain_of_custody_id,
                       created_at=time.time(),
                       consensus_score=r.consensus_score)
        ] + self.audit_log

        error_txt = f" | {len(fc.errors_found)} errors flagged" if fc.errors_found else ""
        self.running = False
        self.status_msg = f"Done — {r.web_sources} web sources{error_txt}."
        self.active_page = "interrogate"
        yield
        await asyncio.sleep(3)
        self.status_msg = ""
        yield
