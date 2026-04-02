"""Base state — all shared vars, routing, computed vars."""
from __future__ import annotations
import asyncio, os
import reflex as rx
from pydantic import BaseModel
from ..backend.mongodb_store import create_user, verify_user, load_user_api_keys, apply_keys_to_env


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
            "interrogate": "/interrogate",
            "vault": "/vault",
            "terminate": "/terminate",
        }
        return rx.redirect(route_map.get(p, "/hub"))

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

        # Load user API keys into environment for backend callers.
        saved_keys = await load_user_api_keys(u)
        apply_keys_to_env(saved_keys)

        self.username = u
        self.authenticated = True
        self.page = "app"
        self.active_page = "hub"
        self.status_msg = ""
        self.login_user = ""
        self.login_pass = ""
        self.show_login_pass = False
        yield
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
        """True only if OpenAI key is actually set in environment."""
        return bool(os.getenv("OPENAI_API_KEY", "").strip())
