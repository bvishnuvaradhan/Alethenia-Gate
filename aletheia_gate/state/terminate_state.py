"""Terminate state."""
import asyncio
from .base import State
from ..backend.vault_db import delete_all

class TermState(State):
    terminating: bool = False

    async def terminate(self):
        self.terminating = True; self.status_msg = "Initiating data scrub..."; yield
        await asyncio.sleep(.8); self.status_msg = "Purging vault records..."; yield
        await delete_all(); await asyncio.sleep(.6)
        self.status_msg = "Severing quantum connection..."; yield
        await asyncio.sleep(.9)
        self.authenticated=False; self.username=""; self.terminating=False
        self.truth_score=0; self.models=[]; self.segments=[]; self.custody_id=""
        self.page="landing"; self.active_page="hub"; self.status_msg=""; yield
