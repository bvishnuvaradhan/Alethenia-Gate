"""Base state — all shared vars, routing, computed vars."""
from __future__ import annotations
import asyncio, os
import reflex as rx
from pydantic import BaseModel
from ..backend.mongodb_store import create_user, verify_user, load_user_api_keys, get_query_results


class ModelStat(BaseModel):
    name: str = ""
    response: str = ""
    score: float = 0.0
    latency: int = 0
    available: bool = True
    error: str = ""
    is_mock: bool = False


class SegmentItem(BaseModel):
    text: str = ""
    status: str = "uncertain"
    reason: str = ""
    confidence: float = 0.5
    explanation: str = ""  # Forensic S-P-O explanation (VOID/VERIFIED/PARTIAL/CRITICAL)
    failed_entities: list[str] = []  # Entities for UI highlighting (pulsing neon magenta)


class AuditEntry(BaseModel):
    prompt: str = ""
    truth_score: int = 0
    custody_id: str = ""
    created_at: float = 0.0
    consensus_score: float = 0.0


class FactErrorItem(BaseModel):
    claim: str = ""
    correction: str = ""
    confidence: float = 0.5
    source: str = ""


class WebSourceItem(BaseModel):
    name: str = ""
    url: str = ""


class State(rx.State):
    # routing
    page: str = "landing"
    active_page: str = "hub"

    # auth
    authenticated: bool = False
    username: str = ""

    # ui
    status_msg: str = ""
    err_msg: str = ""

    # truth engine outputs
    truth_score: int = 0
    consensus: float = 0.0
    semantic: float = 0.0
    alignment: float = 0.0
    custody_id: str = ""
    latency_ms: int = 0
    aggregated_count: int = 0  # Number of results aggregated into dashboard
    models: list[ModelStat] = []
    segments: list[SegmentItem] = []

    # web verification
    web_sources: int = 0
    web_score: float = 0.0
    web_summary: str = ""
    facts_verified: list[str] = []
    facts_unverified: list[str] = []
    web_source_names: list[str] = []   # e.g. ['Wikipedia: Python', 'DuckDuckGo / Wikipedia']
    web_source_urls: list[str] = []    # Corresponding URLs for each source

    # API keys loaded from MongoDB for the active user
    groq_key: str = ""
    gemini_key: str = ""
    cohere_key: str = ""
    anthropic_key: str = ""
    openai_key: str = ""

    # fact checking
    fact_errors: list[FactErrorItem] = []
    fact_checker_used: str = ""
    fact_check_done: bool = False
    fact_penalty: float = 0.0

    # form inputs
    login_user: str = ""
    login_pass: str = ""
    show_login_pass: bool = False
    su_user: str = ""
    su_email: str = ""
    su_pass: str = ""
    show_su_pass: bool = False

    @rx.var
    def web_sources_combined(self) -> list[WebSourceItem]:
        """Combine source names and URLs into list of WebSourceItem objects."""
        names = self.web_source_names or []
        urls = self.web_source_urls or []
        # Create WebSourceItem for each name/url pair
        return [WebSourceItem(name=names[i], url=urls[i] if i < len(urls) else "") for i in range(len(names))]

    # setters
    def set_login_user(self, v: str): self.login_user = v
    def set_login_pass(self, v: str): self.login_pass = v
    def set_su_user(self, v: str):    self.su_user = v
    def set_su_email(self, v: str):   self.su_email = v
    def set_su_pass(self, v: str):    self.su_pass = v
    def toggle_login_pass_visibility(self): self.show_login_pass = not self.show_login_pass
    def toggle_su_pass_visibility(self):    self.show_su_pass = not self.show_su_pass

    def go_landing(self):
        self.page = "landing"
        self.err_msg = ""
        self.show_login_pass = False
        self.show_su_pass = False
        return rx.redirect("/")

    def go_login(self):
        self.page = "login"
        self.err_msg = ""
        self.show_login_pass = False
        return rx.redirect("/login")

    def go_signup(self):
        self.page = "signup"
        self.err_msg = ""
        self.show_su_pass = False
        return rx.redirect("/signup")

    def go_page(self, p: str):
        self.active_page = p
        self.err_msg = ""
        route_map = {
            "hub": "/hub",
            "engine": "/engine",
            "analysis": "/analysis",
            "interrogate": "/interrogate",
            "vault": "/vault",
            "terminate": "/terminate",
        }
        # Refresh aggregated dashboard data in background so sidebar shows
        # up-to-date TRUTH SCORE across all pages for the current user.
        try:
            # Schedule background refresh if running inside an event loop
            asyncio.create_task(self.load_latest_result())
        except Exception:
            # Fallback: ignore if scheduling is not possible in this context
            pass
        return rx.redirect(route_map.get(p, "/hub"))
    
    async def go_hub_with_load(self):
        """Navigate to hub and auto-load dashboard data."""
        await self.load_latest_result()
        self.active_page = "hub"
        yield rx.redirect("/hub")

    async def load_latest_result(self):
        """Load and aggregate ALL user results into dashboard state (averages & combined data)."""
        username = (self.username or "").strip()
        if not username:
            username = "anonymous"
        
        # Fetch all results
        results = await get_query_results(username, limit=100)
        if not results:
            # Try fallback users for backward compatibility
            if username != "anonymous":
                results = await get_query_results("anonymous", limit=100)
            if not results:
                # Clear stale user-specific dashboard state when this user has no data.
                self.truth_score = 0
                self.consensus = 0.0
                self.semantic = 0.0
                self.alignment = 0.0
                self.custody_id = ""
                self.aggregated_count = 0
                self.latency_ms = 0
                self.web_sources = 0
                self.web_score = 0.0
                self.web_summary = ""
                self.facts_verified = []
                self.facts_unverified = []
                self.web_source_names = []
                self.web_source_urls = []
                self.fact_check_done = False
                self.fact_penalty = 0.0
                self.models = []
                self.segments = []
                self.fact_errors = []
                return  # No results to load
        
        # ════ AGGREGATE NUMERIC METRICS ════
        num_results = len(results)
        avg_truth_score = sum(r.get("truth_score", 0) for r in results) / num_results if results else 0
        avg_consensus = sum(r.get("consensus_score", 0.0) for r in results) / num_results if results else 0.0
        avg_semantic = sum(r.get("semantic_similarity", 0.0) for r in results) / num_results if results else 0.0
        avg_alignment = sum(r.get("source_alignment", 0.0) for r in results) / num_results if results else 0.0
        avg_latency = sum(r.get("latency_total", 0) for r in results) / num_results if results else 0
        avg_web_sources = sum(r.get("web_sources", 0) for r in results) / num_results if results else 0
        avg_web_score = sum(r.get("web_score", 0.0) for r in results) / num_results if results else 0.0
        
        # ════ AGGREGATE MODELS (average scores per model name) ════
        model_scores: dict[str, list[dict]] = {}  # {model_name: [list of model data]}
        for result in results:
            for m in result.get("models", []):
                model_name = m.get("name", "Unknown")
                if model_name not in model_scores:
                    model_scores[model_name] = []
                model_scores[model_name].append(m)
        
        # Calculate averages for each model
        aggregated_models = []
        for model_name, model_list in model_scores.items():
            avg_score = sum(float(m.get("score", 0.0)) for m in model_list) / len(model_list) if model_list else 0.0
            avg_latency_model = sum(int(m.get("latency", 0)) for m in model_list) / len(model_list) if model_list else 0
            avg_available = sum(1 for m in model_list if m.get("available", True)) > len(model_list) / 2
            
            aggregated_models.append(
                ModelStat(
                    name=model_name,
                    response="[Aggregated from " + str(len(model_list)) + " queries]",
                    score=round(avg_score, 1),
                    latency=int(avg_latency_model),
                    available=avg_available,
                    error="",
                    is_mock=False
                )
            )
        
        # ════ COMBINE ALL SEGMENTS ════
        all_segments = []
        seen_segment_texts = set()
        for result in results:
            for s in result.get("segments", []):
                segment_text = s.get("text", "")
                # Avoid duplicates
                if segment_text and segment_text not in seen_segment_texts:
                    all_segments.append(
                        SegmentItem(
                            text=segment_text,
                            status=s.get("status", "uncertain"),
                            reason=s.get("reason", ""),
                            confidence=float(s.get("confidence", 0.5)),
                            explanation=s.get("explanation", ""),
                            failed_entities=s.get("failed_entities", [])
                        )
                    )
                    seen_segment_texts.add(segment_text)
        
        # ════ COMBINE ALL FACT ERRORS ════
        all_fact_errors = []
        seen_claims = set()
        for result in results:
            for e in result.get("fact_errors", []):
                claim = e.get("claim", "")
                if claim and claim not in seen_claims:
                    all_fact_errors.append(
                        FactErrorItem(
                            claim=claim,
                            correction=e.get("correction", ""),
                            confidence=float(e.get("confidence", 0.5)),
                            source=e.get("source", "")
                        )
                    )
                    seen_claims.add(claim)
        
        # ════ COMBINE WEB SOURCES ════
        all_web_source_names = []
        all_web_source_urls = []
        seen_sources = set()
        for result in results:
            names = result.get("web_source_names", [])
            urls = result.get("web_source_urls", [])
            for i, name in enumerate(names):
                source_key = (name, urls[i] if i < len(urls) else "")
                if source_key not in seen_sources:
                    all_web_source_names.append(name)
                    all_web_source_urls.append(urls[i] if i < len(urls) else "")
                    seen_sources.add(source_key)
        
        # ════ COMBINE VERIFIED/UNVERIFIED FACTS ════
        all_verified_facts = list(set(f for result in results for f in result.get("facts_verified", [])))
        all_unverified_facts = list(set(f for result in results for f in result.get("facts_unverified", [])))
        
        # ════ POPULATE STATE WITH AGGREGATES ════
        self.truth_score = int(avg_truth_score)
        self.consensus = avg_consensus
        self.semantic = avg_semantic
        self.alignment = avg_alignment
        self.custody_id = f"AGGREGATED_{num_results}_RESULTS"
        self.aggregated_count = num_results
        self.latency_ms = int(avg_latency)
        self.web_sources = int(avg_web_sources)
        self.web_score = avg_web_score
        self.web_summary = f"Aggregated from {num_results} interrogations · {len(all_fact_errors)} unique issues flagged"
        self.facts_verified = all_verified_facts
        self.facts_unverified = all_unverified_facts
        self.web_source_names = all_web_source_names
        self.web_source_urls = all_web_source_urls
        self.fact_check_done = True
        self.fact_penalty = sum(r.get("fact_penalty", 0.0) for r in results) / num_results if results else 0.0
        self.models = aggregated_models
        self.segments = all_segments
        self.fact_errors = all_fact_errors

    async def load_and_go_hub(self):
        """Load latest result and navigate to hub."""
        await self.load_latest_result()
        yield rx.redirect("/hub")



    async def do_login(self):
        u = self.login_user.strip(); p = self.login_pass.strip()
        if not u or not p: self.err_msg = "Both fields required."; return
        self.err_msg = ""; self.status_msg = "Verifying credentials..."; yield

        ok = await verify_user(u, p)
        if not ok:
            self.err_msg = "Invalid username or password."
            self.status_msg = ""
            self.login_pass = ""
            yield
            return

        # Load user API keys into state so all pages can use MongoDB values directly.
        saved_keys = await load_user_api_keys(u)
        self.groq_key = saved_keys.get("groq_key", "") if saved_keys else ""
        self.gemini_key = saved_keys.get("gemini_key", "") if saved_keys else ""
        self.cohere_key = saved_keys.get("cohere_key", "") if saved_keys else ""
        self.anthropic_key = saved_keys.get("anthropic_key", "") if saved_keys else ""
        self.openai_key = saved_keys.get("openai_key", "") if saved_keys else ""

        self.username = u
        self.authenticated = True
        self.page = "app"
        self.active_page = "hub"
        self.status_msg = ""
        self.login_user = ""
        self.login_pass = ""
        self.show_login_pass = False
        # Load aggregated dashboard data for sidebar/dashboard consistency
        yield
        await self.load_latest_result()
        await asyncio.sleep(0.5)
        yield rx.call_script("window.location.href = '/hub'")

    async def do_signup(self):
        u = self.su_user.strip(); e = self.su_email.strip(); p = self.su_pass.strip()
        if not u or not e or not p: self.err_msg = "All fields required."; return
        if len(p) < 6: self.err_msg = "Password too short (min 6 chars)."; return
        self.err_msg = ""; self.status_msg = "Creating operator profile..."; yield

        created, msg = await create_user(u, e, p)
        if not created:
            self.err_msg = msg
            self.status_msg = ""
            yield
            return

        self.username = u
        self.authenticated = True
        self.page = "app"
        self.active_page = "hub"
        self.status_msg = ""
        self.su_user = ""
        self.su_email = ""
        self.su_pass = ""
        self.show_su_pass = False
        yield
        await self.load_latest_result()
        await asyncio.sleep(0.5)
        yield rx.call_script("window.location.href = '/hub'")

    def logout(self):
        self.authenticated = False
        self.username = ""
        self.page = "landing"
        self.active_page = "hub"
        self.status_msg = ""
        self.err_msg = ""
        self.show_login_pass = False
        self.show_su_pass = False
        return rx.redirect("/")

    @rx.var
    def score_color(self) -> str:
        if self.truth_score == 0: return "rgba(220,185,240,.5)"  # dim gray — no data
        if self.truth_score >= 90: return "#00e5a0"   # bright green — verified
        if self.truth_score >= 70: return "#00cfff"   # cyan — low risk
        if self.truth_score >= 40: return "#ffaa00"   # amber — medium risk
        return "#ff0080"                               # pink — high risk

    @rx.var
    def risk_label(self) -> str:
        if self.truth_score == 0: return "NO DATA"
        if self.truth_score >= 90: return "VERIFIED"
        if self.truth_score >= 70: return "LOW RISK"
        if self.truth_score >= 40: return "MEDIUM RISK"
        return "HIGH RISK"

    @rx.var
    def web_score_pct(self) -> str:
        return str(int(self.web_score * 100)) + "%"

    @rx.var
    def has_errors(self) -> bool:
        return len(self.fact_errors) > 0

    @rx.var
    def openai_active(self) -> bool:
        """True only if an OpenAI key is stored for the current user."""
        return bool(getattr(self, "openai_key", "").strip())
