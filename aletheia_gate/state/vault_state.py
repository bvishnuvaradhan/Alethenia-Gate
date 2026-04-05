"""Vault state — loads user's interrogation results from MongoDB."""
import reflex as rx
from .base import State, AuditEntry
from ..backend.mongodb_store import get_query_results


class VaultState(State):
    vault_search: str = ""
    vault_loading: bool = False
    vault_log: list[dict] = []  # Store as dicts for Reflex reactivity
    selected_result: dict = {}  # Store selected result for detail view

    def set_search(self, v: str):
        self.vault_search = v

    async def load(self):
        """Load all user's query results from MongoDB."""
        self.vault_loading = True
        yield

        username = self.username or "anonymous"
        entries = await get_query_results(username, limit=100)

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

    def select_result(self, custody_id: str):
        """Select a result to view details."""
        # Find the result and store it
        for entry in self.vault_log:
            if entry["custody_id"] == custody_id:
                self.selected_result = {
                    "custody_id": entry["custody_id"],
                    "prompt": entry["prompt"],
                    "truth_score": entry["truth_score"],
                }
                break
        return rx.redirect(f"/vault?id={custody_id}")

    # Called whenever the vault page is shown
    def go_vault(self):
        self.active_page = "vault"
        self.err_msg = ""
        return rx.redirect("/vault")
