"""
Rate limiter for APIs with daily/monthly limits.

NewsAPI:      100 req/day  (free tier)
Cohere:       1000 req/month (free tier)
"""
import asyncio, json, os, time
from pathlib import Path

_STORE: dict = {}   # in-memory counter

class RateLimit:
    def __init__(self, key: str, limit: int, window_seconds: int):
        self.key     = key
        self.limit   = limit
        self.window  = window_seconds   # 86400 = daily, 2592000 = monthly

    def check(self) -> tuple[bool, int]:
        """Returns (allowed, remaining). Thread-safe for single-process."""
        now    = time.time()
        bucket = _STORE.setdefault(self.key, {"count": 0, "reset_at": now + self.window})

        # Reset window if expired
        if now >= bucket["reset_at"]:
            bucket["count"]    = 0
            bucket["reset_at"] = now + self.window

        remaining = self.limit - bucket["count"]
        if remaining <= 0:
            return False, 0

        bucket["count"] += 1
        return True, remaining - 1

    def remaining(self) -> int:
        now    = time.time()
        bucket = _STORE.get(self.key, {"count": 0, "reset_at": now})
        if now >= bucket["reset_at"]:
            return self.limit
        return max(0, self.limit - bucket["count"])

    def reset_in(self) -> int:
        """Seconds until counter resets."""
        bucket = _STORE.get(self.key, {})
        return max(0, int(bucket.get("reset_at", time.time()) - time.time()))


# ── Pre-built limiters ────────────────────────────────────────────────────────
NEWSAPI_LIMIT  = RateLimit("newsapi",   100,  86400)    # 100/day
COHERE_LIMIT   = RateLimit("cohere",    1000, 2592000)  # 1000/month

def get_status() -> dict:
    """Return current usage for all rate-limited APIs."""
    return {
        "newsapi":  {"remaining": NEWSAPI_LIMIT.remaining(),  "limit": 100,  "period": "day",   "reset_in_sec": NEWSAPI_LIMIT.reset_in()},
        "cohere":   {"remaining": COHERE_LIMIT.remaining(),   "limit": 1000, "period": "month", "reset_in_sec": COHERE_LIMIT.reset_in()},
    }
