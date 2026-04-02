"""Vault state — auto-loads when page is navigated to."""
import reflex as rx
from .base import State, AuditEntry
from ..backend.vault_db import get_audit_log


class VaultState(State):
    vault_search: str = ""
    vault_loading: bool = False
    vault_log: list[AuditEntry] = []

    def set_search(self, v: str):
        self.vault_search = v

    async def load(self):
        self.vault_loading = True
        yield
        entries = await get_audit_log(100, self.vault_search.strip() or None)
        self.vault_log = [
            AuditEntry(
                prompt=e.get("prompt", "")[:80],
                truth_score=e.get("truth_score", 0),
                custody_id=e.get("chain_of_custody_id", ""),
                created_at=float(e.get("created_at", 0)),
                consensus_score=float(e.get("consensus_score", 0)),
            )
            for e in entries
        ]
        self.vault_loading = False
        yield

    async def search(self):
        await self.load()

    # Called whenever the vault page is shown
    def go_vault(self):
        self.active_page = "vault"
        self.err_msg = ""
        return rx.redirect("/vault")
