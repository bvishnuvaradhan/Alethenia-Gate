"""MongoDB persistence for users and per-user API keys."""
from __future__ import annotations

import asyncio
import hashlib
import os
import secrets
import urllib.parse
from typing import Any

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    _PYMONGO_AVAILABLE = True
except Exception:
    MongoClient = None  # type: ignore[assignment]
    PyMongoError = Exception  # type: ignore[assignment]
    _PYMONGO_AVAILABLE = False


_DB_NAME = "aletheia_gate"
_USERS = "users"
_API_KEYS = "api_keys"
_RESULTS = "query_results"

_client: Any = None


def _mongo_uri() -> str:
    raw = os.getenv("MONGODB_URI", "").strip()
    if not raw:
        return ""

    # Accept user-provided form with <password> and auto-encode special chars.
    # Example:
    # mongodb+srv://user:<My@Pass>@cluster.mongodb.net/?appName=Cluster0
    # -> mongodb+srv://user:My%40Pass@cluster.mongodb.net/?appName=Cluster0
    try:
        if not (raw.startswith("mongodb://") or raw.startswith("mongodb+srv://")):
            return raw
        scheme, rest = raw.split("://", 1)
        if "@" not in rest:
            return raw
        # Split from the right so '@' inside password is preserved.
        creds, tail = rest.rsplit("@", 1)
        if ":" not in creds:
            return raw
        user, pwd = creds.split(":", 1)

        pwd = pwd.strip()
        if pwd.startswith("<") and pwd.endswith(">"):
            pwd = pwd[1:-1]

        # If password is not already URL-encoded, encode it.
        if "%" not in pwd:
            pwd = urllib.parse.quote(pwd, safe="")

        return f"{scheme}://{user}:{pwd}@{tail}"
    except Exception:
        return raw


def _get_client() -> Any:
    global _client
    if not _PYMONGO_AVAILABLE:
        raise RuntimeError("pymongo is not installed")
    if _client is None:
        uri = _mongo_uri()
        if not uri:
            raise RuntimeError("MONGODB_URI is not configured")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # force connect early
        _client.admin.command("ping")
    return _client


def _db():
    return _get_client()[_DB_NAME]


def _hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return salt.hex(), digest.hex()


def _ensure_indexes_sync() -> None:
    db = _db()
    db[_USERS].create_index("username", unique=True)
    db[_USERS].create_index("email", unique=True)
    db[_API_KEYS].create_index("username", unique=True)
    # Results indexes - for fast lookup by username and timestamp
    db[_RESULTS].create_index("username")
    db[_RESULTS].create_index("created_at", sparse=True)
    db[_RESULTS].create_index([("username", 1), ("created_at", -1)])


def _create_user_sync(username: str, email: str, password: str) -> tuple[bool, str]:
    _ensure_indexes_sync()
    users = _db()[_USERS]

    if users.find_one({"username": username}):
        return False, "Username already exists."
    if users.find_one({"email": email}):
        return False, "Email already exists."

    salt, pw_hash = _hash_password(password)
    users.insert_one(
        {
            "username": username,
            "email": email,
            "password_hash": pw_hash,
            "salt": salt,
        }
    )
    return True, "ok"


def _verify_user_sync(username: str, password: str) -> bool:
    user = _db()[_USERS].find_one({"username": username})
    if not user:
        return False
    salt = user.get("salt", "")
    pw_hash = user.get("password_hash", "")
    if not salt or not pw_hash:
        return False
    _, calc_hash = _hash_password(password, salt)
    return secrets.compare_digest(calc_hash, pw_hash)


def _save_user_api_keys_sync(username: str, keys: dict[str, str]) -> bool:
    _ensure_indexes_sync()
    _db()[_API_KEYS].update_one(
        {"username": username},
        {"$set": {"username": username, "keys": keys}},
        upsert=True,
    )
    return True


def _load_user_api_keys_sync(username: str) -> dict[str, str]:
    doc = _db()[_API_KEYS].find_one({"username": username}) or {}
    keys = doc.get("keys", {})
    return keys if isinstance(keys, dict) else {}


async def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    if not _PYMONGO_AVAILABLE:
        return False, "Database unavailable. Install pymongo in server environment."
    try:
        return await asyncio.to_thread(_create_user_sync, username, email, password)
    except (PyMongoError, RuntimeError):
        return False, "Database unavailable. Check MONGODB_URI (encode special chars like @ as %40)."


async def verify_user(username: str, password: str) -> bool:
    if not _PYMONGO_AVAILABLE:
        return False
    try:
        return await asyncio.to_thread(_verify_user_sync, username, password)
    except (PyMongoError, RuntimeError):
        return False


async def save_user_api_keys(username: str, keys: dict[str, str]) -> bool:
    if not username:
        return False
    if not _PYMONGO_AVAILABLE:
        return False
    try:
        return await asyncio.to_thread(_save_user_api_keys_sync, username, keys)
    except (PyMongoError, RuntimeError):
        return False


async def load_user_api_keys(username: str) -> dict[str, str]:
    if not username:
        return {}
    if not _PYMONGO_AVAILABLE:
        return {}
    try:
        return await asyncio.to_thread(_load_user_api_keys_sync, username)
    except (PyMongoError, RuntimeError):
        return {}


def save_user_api_keys_now(username: str, keys: dict[str, str]) -> bool:
    """Sync helper for setter methods."""
    if not username:
        return False
    if not _PYMONGO_AVAILABLE:
        return False
    try:
        return _save_user_api_keys_sync(username, keys)
    except (PyMongoError, RuntimeError):
        return False


def apply_keys_to_env(keys: dict[str, Any]) -> None:
    mapping = {
        "groq_key": "GROQ_API_KEY",
        "gemini_key": "GEMINI_API_KEY",
        "cohere_key": "COHERE_API_KEY",
        "anthropic_key": "ANTHROPIC_API_KEY",
        "openai_key": "OPENAI_API_KEY",
    }
    for state_key, env_key in mapping.items():
        val = str(keys.get(state_key, "") or "").strip()
        if val:
            os.environ[env_key] = val
        else:
            os.environ.pop(env_key, None)


def _save_query_result_sync(username: str, result_data: dict[str, Any]) -> tuple[bool, str]:
    """Save interrogation result to MongoDB."""
    try:
        _ensure_indexes_sync()
        result_doc = {
            "username": username,
            "created_at": result_data.get("created_at"),
            "prompt": result_data.get("prompt"),
            "truth_score": result_data.get("truth_score"),
            "consensus_score": result_data.get("consensus_score"),
            "semantic_similarity": result_data.get("semantic_similarity"),
            "source_alignment": result_data.get("source_alignment"),
            "chain_of_custody_id": result_data.get("chain_of_custody_id"),
            "latency_total": result_data.get("latency_total"),
            "web_sources": result_data.get("web_sources"),
            "web_score": result_data.get("web_score"),
            "web_summary": result_data.get("web_summary"),
            "facts_verified": result_data.get("facts_verified", []),
            "facts_unverified": result_data.get("facts_unverified", []),
            "web_source_names": result_data.get("web_source_names", []),
            "web_source_urls": result_data.get("web_source_urls", []),
            "models": result_data.get("models", []),
            "segments": result_data.get("segments", []),
            "fact_errors": result_data.get("fact_errors", []),
            "fact_check_done": result_data.get("fact_check_done"),
            "fact_penalty": result_data.get("fact_penalty"),
        }
        _db()[_RESULTS].insert_one(result_doc)
        return True, result_data.get("chain_of_custody_id", "")
    except PyMongoError as e:
        return False, str(e)


def _get_query_results_sync(username: str, limit: int = 50) -> list[dict]:
    """Retrieve recent query results for user."""
    try:
        _ensure_indexes_sync()
        results = list(
            _db()[_RESULTS]
            .find({"username": username})
            .sort("created_at", -1)
            .limit(limit)
        )
        # Convert ObjectId to string for JSON serialization
        for r in results:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        return results
    except PyMongoError:
        return []


def _get_query_result_by_id_sync(username: str, custody_id: str) -> dict | None:
    """Retrieve specific query result by custody ID."""
    try:
        _ensure_indexes_sync()
        result = _db()[_RESULTS].find_one(
            {"username": username, "chain_of_custody_id": custody_id}
        )
        if result and "_id" in result:
            result["_id"] = str(result["_id"])
        return result
    except PyMongoError:
        return None


async def save_query_result(username: str, result_data: dict[str, Any]) -> tuple[bool, str]:
    """Async wrapper for saving query results."""
    if not username:
        return False, "No username provided"
    if not _PYMONGO_AVAILABLE:
        return False, "MongoDB not available"
    try:
        return await asyncio.to_thread(_save_query_result_sync, username, result_data)
    except Exception as e:
        return False, str(e)


async def get_query_results(username: str, limit: int = 50) -> list[dict]:
    """Async wrapper for retrieving query results."""
    if not username:
        return []
    if not _PYMONGO_AVAILABLE:
        return []
    try:
        return await asyncio.to_thread(_get_query_results_sync, username, limit)
    except Exception:
        return []


async def get_query_result_by_id(username: str, custody_id: str) -> dict | None:
    """Async wrapper for retrieving specific query result."""
    if not username or not custody_id:
        return None
    if not _PYMONGO_AVAILABLE:
        return None
    try:
        return await asyncio.to_thread(_get_query_result_by_id_sync, username, custody_id)
    except Exception:
        return None
