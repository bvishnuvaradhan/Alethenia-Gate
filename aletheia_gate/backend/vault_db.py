"""Vault — in-memory store (SurrealDB optional)."""
import time
_store: list[dict] = []

async def init_schema(): pass

async def save_audit(entry: dict):
    entry.setdefault("created_at", time.time())
    _store.insert(0, dict(entry))
    if len(_store) > 500: _store.pop()

async def get_audit_log(limit=100, search=None):
    r = _store[:limit]
    if search:
        s = search.lower()
        r = [e for e in r if s in e.get("prompt","").lower()]
    return r

async def delete_all(): _store.clear()
