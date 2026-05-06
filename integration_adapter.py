"""
integration_adapter.py
NICAI — Task 5 Integration (Sanskar Pandey)

PURPOSE:
  - Converts NICAI signal format -> SanskarEngine input format
  - Calls SanskarEngine.process()
  - Converts SanskarEngine output -> NICAI output contract

INPUT CONTRACT (from NICAI /nicai/evaluate):
  {
    "signal_id": "...", "status": "...", "confidence_score": ...,
    "trace_id": "...", "reason": "...",
    "value": { "temperature": ..., "aqi": ... },
    "timestamp": "...", "location": "..."
  }

OUTPUT CONTRACT (to NICAI dashboard and API):
  {
    "risk_level", "anomaly_type", "explanation",
    "temporal_context", "spatial_context",
    "confidence", "recommendation_signal"
  }

RULES:
  - ONLY process ALLOW / VALID / FLAG
  - IGNORE REJECT signals (return status=IGNORED)
  - NEVER crash - always return a dict
"""

from sanskar_engine import SanskarEngine

# Singleton engine - created once at module load
engine = SanskarEngine()


def map_nicai_to_engine_input(signal: dict) -> dict:
    """Convert NICAI signal dict -> SanskarEngine.process() input dict."""
    value = signal.get("value") or {}

    if isinstance(value, dict):
        try:
            temperature = float(value.get("temperature", 0) or 0)
        except (TypeError, ValueError):
            temperature = 0.0
        try:
            pollution = float(value.get("aqi", 0) or 0)
        except (TypeError, ValueError):
            pollution = 0.0
    else:
        # flat numeric fallback - treat as AQI
        try:
            pollution = float(value or 0)
        except (TypeError, ValueError):
            pollution = 0.0
        temperature = 0.0

    try:
        trend = float(signal.get("trend", 0.5) or 0.5)
    except (TypeError, ValueError):
        trend = 0.5

    location = signal.get("location") or signal.get("city") or "unknown"

    return {
        "temperature": temperature,
        "pollution": pollution,
        "trend": trend,
        "zone": [str(location)],
    }


def map_engine_to_nicai_output(engine_output: dict) -> dict:
    """Normalize SanskarEngine output -> NICAI API/dashboard contract."""
    risk = engine_output.get("risk_level", "LOW")
    anomaly = engine_output.get("anomaly_type", "normal")
    explanation = engine_output.get("explanation", "No issue detected.")
    temporal = engine_output.get("temporal_context", "STABLE")
    spatial = engine_output.get("spatial_context", "unknown")
    confidence = engine_output.get("confidence_score", 0.5)

    recommendation = engine_output.get("recommendation_signal")
    if not recommendation:
        if risk == "HIGH":
            recommendation = "eligible_for_escalation"
        elif risk == "MEDIUM":
            recommendation = "requires_review"
        else:
            recommendation = "monitor"

    return {
        "risk_level": str(risk),
        "anomaly_type": str(anomaly),
        "explanation": str(explanation),
        "temporal_context": str(temporal),
        "spatial_context": str(spatial),
        "confidence": float(confidence),
        "recommendation_signal": str(recommendation),
    }


def run_engine(signal: dict) -> dict:
    """
    Full adapter pipeline called by all API routes.
    1. Check signal is processable
    2. Map input
    3. Run SanskarEngine
    4. Map output to NICAI contract
    Never raises - always returns a dict.
    """
    try:
        if not isinstance(signal, dict) or not signal:
            return {"status": "ERROR", "reason": "Invalid signal: must be non-empty dict"}

        # PHASE 2: REJECT signals are ignored
        if signal.get("status") == "REJECT":
            return {"status": "IGNORED", "reason": "Signal status is REJECT"}

        engine_input = map_nicai_to_engine_input(signal)
        engine_output = engine.process(engine_input)

        if not isinstance(engine_output, dict):
            return {"status": "ERROR", "reason": "SanskarEngine returned invalid output"}

        output = map_engine_to_nicai_output(engine_output)

        # PHASE 4 — TRACE CONTINUITY
        output["trace_id"] = signal.get("trace_id", "unknown")

        return output

    except Exception as e:
        return {"status": "ERROR", "reason": f"Engine adapter exception: {str(e)}"}
