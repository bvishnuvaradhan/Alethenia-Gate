"""Engine Room state — all free API keys."""
import asyncio
import json
import urllib.request
import reflex as rx
from .base import State
from ..backend.mongodb_store import save_user_api_keys_now, load_user_api_keys


class EngineState(State):
    # Settings
    sensitivity: int = 75
    max_tokens:  int = 800
    temp_x10:    int = 2
    tog_temporal: bool = True
    tog_semantic: bool = True
    tog_factual:  bool = False
    tog_realtime: bool = True

    # Gemini active model (set after cascade succeeds)
    gemini_active_model: str = ""

    def _api_payload(self) -> dict[str, str]:
        return {
            "groq_key": self.groq_key,
            "gemini_key": self.gemini_key,
            "cohere_key": self.cohere_key,
            "anthropic_key": self.anthropic_key,
            "openai_key": self.openai_key,
        }

    def _persist_api_keys(self):
        if self.authenticated and self.username:
            save_user_api_keys_now(self.username, self._api_payload())

    def set_groq(self, v: str):
        self.groq_key = v; self._persist_api_keys()

    def set_gemini(self, v: str):
        self.gemini_key = v; self._persist_api_keys()

    def set_cohere(self, v: str):
        self.cohere_key = v; self._persist_api_keys()

    def set_anthropic(self, v: str):
        self.anthropic_key = v; self._persist_api_keys()

    def set_openai(self, v: str):
        self.openai_key = v; self._persist_api_keys()

    async def load_saved_api_keys(self):
        if not self.authenticated or not self.username:
            self.groq_key = ""
            self.gemini_key = ""
            self.cohere_key = ""
            self.anthropic_key = ""
            self.openai_key = ""
            return
        keys = await load_user_api_keys(self.username)
        self.groq_key = keys.get("groq_key", "") if keys else ""
        self.gemini_key = keys.get("gemini_key", "") if keys else ""
        self.cohere_key = keys.get("cohere_key", "") if keys else ""
        self.anthropic_key = keys.get("anthropic_key", "") if keys else ""
        self.openai_key = keys.get("openai_key", "") if keys else ""
        # Do NOT mirror DB-stored keys into process env.
        # Keys from MongoDB will be used from state only (no .env fallback).

    def set_sens(self, v):
        if isinstance(v, (list, tuple)):
            v = v[0] if v else self.sensitivity
        try:
            self.sensitivity = max(0, min(100, int(v)))
        except (TypeError, ValueError):
            pass
    def set_tokens(self, v: int): self.max_tokens  = v
    def set_temp(self, v: int):   self.temp_x10    = v

    def tog(self, k: str):
        if   k == "temporal": self.tog_temporal = not self.tog_temporal
        elif k == "semantic":  self.tog_semantic = not self.tog_semantic
        elif k == "factual":   self.tog_factual  = not self.tog_factual
        elif k == "realtime":  self.tog_realtime = not self.tog_realtime

    async def verify(self):
        self.status_msg = "Verifying connections..."
        yield
        results = []

        # Use keys ONLY from state (loaded from MongoDB). Do not use env fallbacks.
        groq_k = self.groq_key.strip()
        gemini_k = self.gemini_key.strip()
        cohere_k = self.cohere_key.strip()
        anthropic_k = self.anthropic_key.strip()
        openai_k = self.openai_key.strip()
        # Mirror env-derived keys back to state so UI reflects actual loaded values.
        self.groq_key = groq_k
        self.gemini_key = gemini_k
        self.cohere_key = cohere_k
        self.anthropic_key = anthropic_k
        self.openai_key = openai_k

        from aletheia_gate.backend.free_models import (
            call_groq,
            call_gemini,
            call_cohere,
            call_anthropic,
            call_openai,
        )

        # Groq
        if groq_k:
            gq = await call_groq("OK", max_tokens=8, api_key=groq_k)
            results.append("Groq ✓" if gq.available else f"Groq ✗ ({(gq.error or 'unavailable')[:42]})")
        else:
            results.append("Groq — no key")

        # Gemini (skip verification due to quota exhaustion, key stored in MongoDB)
        if gemini_k:
            results.append("Gemini ✓ (key set, skipped verification)")
        else:
            results.append("Gemini — no key")

        # Cohere
        if cohere_k:
            ch = await call_cohere("OK", max_tokens=8, api_key=cohere_k)
            results.append("Cohere ✓" if ch.available else f"Cohere ✗ ({(ch.error or 'unavailable')[:42]})")
        else:
            results.append("Cohere — no key")

        # Anthropic
        if anthropic_k:
            an = await call_anthropic("OK", max_tokens=8, api_key=anthropic_k)
            results.append("Anthropic ✓" if an.available else f"Anthropic ✗ ({(an.error or 'unavailable')[:42]})")
        else:
            results.append("Anthropic — no key")

        # OpenAI (optional)
        if openai_k:
            oa = await call_openai("OK", max_tokens=8, api_key=openai_k)
            results.append("OpenAI ✓" if oa.available else f"OpenAI ✗ ({(oa.error or 'unavailable')[:42]})")
        else:
            results.append("OpenAI — no key")

        self.status_msg = " | ".join(results)
        yield
        await asyncio.sleep(6)
        self.status_msg = ""
        yield

    @rx.var
    def temp_display(self) -> str:
        return f"{self.temp_x10 / 10:.1f}"

    @rx.var
    def gemini_display(self) -> str:
        if self.gemini_active_model:
            return f"Active: {self.gemini_active_model}"
        return "Will cascade: 2.5-pro-preview → 2.5-pro → 2.5-flash → 2.5-flash-lite"
