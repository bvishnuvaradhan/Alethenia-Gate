"""
Safety wrappers for verification to prevent hangs, errors, and duplicate calls.
"""
import asyncio
from functools import lru_cache
from typing import Any

# ─── Timeouts ───────────────────────────────────────────────────────────────

async def safe_verify(coro, timeout_sec: int = 12):
    """
    Wrap any async operation with timeout protection.

    Prevents hanging if APIs are slow or unresponsive.
    """
    try:
        result = await asyncio.wait_for(coro, timeout=timeout_sec)
        return result
    except asyncio.TimeoutError:
        return {
            "error": f"⏱️ Request timed out after {timeout_sec}s",
            "status": "timeout"
        }
    except Exception as e:
        return {
            "error": f"❌ Error: {str(e)[:100]}",
            "status": "error",
            "details": str(e)
        }


# ─── Result Caching (optional speedup) ──────────────────────────────────────

_verification_cache = {}

def cache_result(prompt: str, result: Any):
    """Store verification result in memory cache."""
    _verification_cache[prompt[:100]] = result

def get_cached_result(prompt: str):
    """Retrieve cached result if available."""
    return _verification_cache.get(prompt[:100], None)

def clear_cache():
    """Clear verification cache."""
    global _verification_cache
    _verification_cache = {}


# ─── Error Message Formatter ────────────────────────────────────────────────

def format_error(error_dict: dict) -> str:
    """Convert error dict to user-friendly message."""
    if isinstance(error_dict, dict):
        return error_dict.get("error", "Unknown error")
    return str(error_dict)


# ─── Validation Helpers ────────────────────────────────────────────────────

def is_valid_prompt(prompt: str) -> tuple[bool, str]:
    """Validate prompt before submission."""
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty"
    if len(prompt) < 5:
        return False, "Prompt too short (minimum 5 characters)"
    if len(prompt) > 5000:
        return False, "Prompt too long (maximum 5000 characters)"
    return True, ""


# ─── Safe Execution Wrapper ────────────────────────────────────────────────

async def safe_execute(
    coro,
    timeout_sec: int = 12,
    operation_name: str = "Operation"
) -> dict:
    """
    Safely execute async operation with full error handling.

    Returns dict with:
      - success: bool
      - result: any (if success)
      - error: str (if failed)
      - status: "ok" | "timeout" | "error"
    """
    try:
        result = await asyncio.wait_for(coro, timeout=timeout_sec)
        return {
            "success": True,
            "result": result,
            "status": "ok"
        }
    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"⏱️ {operation_name} timed out after {timeout_sec}s",
            "status": "timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"❌ {operation_name} failed: {str(e)[:100]}",
            "status": "error",
            "details": str(e)
        }
