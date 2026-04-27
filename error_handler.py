"""
error_handler.py — NICAI Phase 8: Failure Hardening
Sanskar Pandey

Ensures system NEVER crashes:
  - error_response()       -> structured error dict (always safe)
  - validate_basic_input() -> input gate for batch operations
  - safe_float()           -> cast value to float without crash
  - safe_str()             -> cast value to str without crash
"""

import hashlib
from datetime import datetime, timezone


def generate_error_trace_id(message: str) -> str:
    """Generate a deterministic trace ID from error message."""
    return "err_" + hashlib.sha256(str(message).encode()).hexdigest()[:12]


def error_response(reason, trace_id=None) -> dict:
    """
    Return a structured error dict. NEVER raises.
    Always includes: status, reason, trace_id, timestamp.
    """
    reason = str(reason)
    return {
        "status": "ERROR",
        "reason": reason,
        "trace_id": trace_id or generate_error_trace_id(reason),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def validate_basic_input(data) -> dict | None:
    """
    Gate check for batch inputs.
    Returns error_response dict if input is invalid, else None (pass).
    """
    if data is None:
        return error_response("Input is None")

    if not isinstance(data, (list, dict)):
        return error_response("Input must be list or dict")

    if isinstance(data, list) and len(data) == 0:
        return error_response("Empty input list")

    if isinstance(data, dict) and len(data) == 0:
        return error_response("Empty input object")

    return None  # passes


def safe_float(value, default: float = 0.0) -> float:
    """Cast value to float without crashing. Returns default on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_str(value, default: str = "") -> str:
    """Cast value to str without crashing. Returns default on None."""
    if value is None:
        return default
    return str(value)
