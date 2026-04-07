"""Vault state — loads user's interrogation results from MongoDB."""
import reflex as rx
from .base import State, AuditEntry
from ..backend.mongodb_store import get_query_results, backfill_query_results
from typing import List, Dict


class VaultState(State):
    vault_search: str = ""
    vault_loading: bool = False
    vault_log: list[dict] = []  # Store as dicts for Reflex reactivity
    selected_result: dict = {}  # Store selected result for detail view
    show_modal: bool = False  # Show/hide detail modal
    modal_data: dict = {}  # Full result data for modal display
    # Typed modal lists for Reflex foreach rendering
    modal_facts_verified: List[str] = []
    modal_facts_unverified: List[str] = []
    modal_models: List[Dict] = []
    modal_web_sources_paired: List[Dict] = []
    modal_segments: List[Dict] = []
    modal_fact_errors: List[Dict] = []
    vault_backfill_done: bool = False

    def set_search(self, v: str):
        self.vault_search = v

    async def load(self):
        """Load all user's query results from MongoDB."""
        self.vault_loading = True
        yield

        username = (self.username or "").strip()
        primary_user = username or "anonymous"

        # One-time backfill for legacy entries so detail modal has fuller content.
        if not self.vault_backfill_done:
            await backfill_query_results(primary_user, limit=500)
            self.vault_backfill_done = True

        entries = await get_query_results(primary_user, limit=100)

        # Backward compatibility: older sessions may have been saved under
        # lowercase username or anonymous before auth was configured.
        if not entries:
            fallback_users: list[str] = []
            if username and username.lower() != primary_user:
                fallback_users.append(username.lower())
            if primary_user != "anonymous":
                fallback_users.append("anonymous")

            merged: dict[str, dict] = {}
            for fb_user in fallback_users:
                for item in await get_query_results(fb_user, limit=100):
                    custody_id = str(item.get("chain_of_custody_id", "")).strip()
                    key = custody_id or str(item.get("_id", ""))
                    if key and key not in merged:
                        merged[key] = item

            entries = sorted(
                merged.values(),
                key=lambda x: float(x.get("created_at", 0.0) or 0.0),
                reverse=True,
            )[:100]

        self.vault_log = [
            {
                "custody_id": e.get("chain_of_custody_id", ""),
                "prompt": e.get("prompt", "")[:100],
                "truth_score": int(e.get("truth_score", 0)),
                "consensus_score": float(e.get("consensus_score", 0.0)),
                "web_sources": int(e.get("web_sources", 0)),
                "web_score": float(e.get("web_score", 0.0)),
                "latency_total": int(e.get("latency_total", 0)),
                "created_at": float(e.get("created_at", 0.0)),
                "facts_verified": len(e.get("facts_verified", [])),
                "facts_unverified": len(e.get("facts_unverified", [])),
                "segments_count": len(e.get("segments", [])),
                "fact_errors_count": len(e.get("fact_errors", [])),
            }
            for e in entries
        ]

        self.vault_loading = False
        yield

    async def search(self):
        """Search through loaded results (client-side filtering)."""
        await self.load()

    async def select_result(self, custody_id: str):
        """Fetch and display full result details in modal."""
        from ..backend.mongodb_store import get_query_result_by_id
        
        username = (self.username or "").strip() or "anonymous"
        result = await get_query_result_by_id(username, custody_id)
        
        if not result:
            # Try fallback user
            if username != "anonymous":
                result = await get_query_result_by_id("anonymous", custody_id)
        
        if result:
            # Format modal data with pre-calculated percentages
            consensus_pct = int(result.get("consensus_score", 0.0) * 100)
            web_score_pct = int(result.get("web_score", 0.0) * 100)
            models = result.get("models", [])

            # Prefer persisted final output; then web summary; then stream output; fallback to first model response.
            final_output = str(result.get("final_output", "") or "").strip()
            if not final_output:
                # Prefer primary streamed response when present
                final_output = str(result.get("stream_output", "") or "").strip()
            if not final_output:
                final_output = str(result.get("web_summary", "") or "").strip()
            if not final_output:
                for m in models:
                    response = str(m.get("response", "") or "").strip() if isinstance(m, dict) else ""
                    if response:
                        final_output = response
                        break
            
            # Pair web sources (names with URLs)
            web_names = result.get("web_source_names", [])
            web_urls = result.get("web_source_urls", [])
            web_sources_paired = []
            for i, name in enumerate(web_names):
                url = web_urls[i] if i < len(web_urls) else "https://example.com"
                web_sources_paired.append({"name": name, "url": url})

            # Heuristic: if prompt looks like a math/pure-fact question, prefer math-related sources
            import re
            prompt_text = (result.get("prompt", "") or "").lower()
            is_math_like = bool(re.search(r"\bsolve\b|\bfind x\b|\bx\^|\d+\s*[\+\-\*\/]\s*\d+|\\^", prompt_text))
            if is_math_like:
                math_tokens = ["math", "symbolab", "wolfram", "calculator", "stackexchange", "mathway", "wikipedia"]
                filtered = [s for s in web_sources_paired if any(t in (s.get("name", "") + s.get("url", "")).lower() for t in math_tokens)]
                if filtered:
                    web_sources_paired = filtered
            
            self.modal_data = {
                "custody_id": result.get("chain_of_custody_id", ""),
                "prompt": result.get("prompt", ""),
                "truth_score": result.get("truth_score", 0),
                "consensus_score_pct": f"{consensus_pct}%",
                "web_sources": result.get("web_sources", 0),
                "web_score_pct": f"{web_score_pct}%",
                "latency_total": result.get("latency_total", 0),
                "facts_verified": result.get("facts_verified", []),
                "facts_unverified": result.get("facts_unverified", []),
                "web_source_names": result.get("web_source_names", []),
                "web_source_urls": result.get("web_source_urls", []),
                "web_sources_paired": web_sources_paired,
                "fact_errors": result.get("fact_errors", []),
                "models": models,
                "segments": result.get("segments", []),
                "web_summary": result.get("web_summary", ""),
                "final_output": final_output,
                "stream_output": result.get("stream_output", ""),
            }
            # Also set typed list state vars so Reflex can foreach over them
            self.modal_facts_verified = result.get("facts_verified", [])
            self.modal_facts_unverified = result.get("facts_unverified", [])
            self.modal_models = models
            self.modal_web_sources_paired = web_sources_paired
            self.modal_segments = result.get("segments", [])
            self.modal_fact_errors = result.get("fact_errors", [])
            self.show_modal = True
            yield

    async def delete_result(self, custody_id: str):
        """Delete a saved query from MongoDB and update local vault list."""
        from ..backend.mongodb_store import delete_query_result

        if not custody_id:
            return
        # optimistic UI: close modal and show loading
        self.show_modal = False
        self.vault_loading = True
        yield

        username = (self.username or "").strip() or "anonymous"
        ok = await delete_query_result(username, custody_id)

        # Refresh local list: remove item if deletion succeeded
        if ok:
            self.vault_log = [e for e in self.vault_log if (e.get("custody_id") or "") != custody_id]
        else:
            # failed deletion — keep log but set error
            self.err_msg = "Failed to delete record from DB"

        self.vault_loading = False
        yield
    
    def close_modal(self):
        """Close the detail modal."""
        self.show_modal = False

    # Called whenever the vault page is shown
    def go_vault(self):
        self.active_page = "vault"
        self.err_msg = ""
        return rx.redirect("/vault")
