"""
main.py — NICAI FastAPI Application (Task 5 — Full Integration)
Sanskar Pandey

ROUTES:
  GET  /test                -> health check
  POST /validate            -> validate a single signal
  POST /pipeline            -> validate + run Sanskar Engine
  POST /nicai/evaluate      -> official NICAI evaluation endpoint (primary)
  GET  /run                 -> batch run on CSV datasets
  GET  /dashboard           -> HTML dashboard with live engine output
  POST /action              -> log an action (Escalate/Review/Assign)

INTEGRATION:
  SamacharInputAdapter -> Validation -> IntegrationAdapter -> SanskarEngine -> Output
"""

print("NICAI main.py loaded — Task 5 integration active")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
import json
import os
import uuid
from integration_orchestrator import orchestrate_intelligence
#from integration_adapter import run_engine
from samachar_input_adapter import load_data, convert_to_signals
from error_handler import error_response, validate_basic_input

# -------------------------------------------------------
# Ensure log directory exists
# -------------------------------------------------------
os.makedirs("logs", exist_ok=True)

app = FastAPI(title="NICAI Intelligence Engine", version="5.0")
templates = Jinja2Templates(directory="templates")


# -------------------------------------------------------
# INTERNAL: Validation (real, not mocked)
# Phase 1: old analyze_signal() fully bypassed — uses SanskarEngine via run_engine()
# -------------------------------------------------------
def validate_signal(signal: dict):
    """
    Validate a NICAI signal dict.
    Returns structured validated dict with status=VALID, or ERROR dict, or None (REJECT).
    """
    if not isinstance(signal, dict) or not signal:
        return {"status": "ERROR", "reason": "Input must be non-empty dict"}

    if not signal.get("signal_id"):
        return {"status": "ERROR", "reason": "Missing signal_id"}

    if not signal.get("timestamp"):
        return {"status": "ERROR", "reason": "Missing timestamp"}

    # PHASE 2 RULE: REJECT signals are silently dropped
    if signal.get("status") == "REJECT":
        return None

    if signal.get("value") is None:
        return {"status": "ERROR", "reason": "Missing value"}
    value = signal.get("value")

# must be dict
    if not isinstance(value, dict):
        return {
            "status": "ERROR",
            "reason": "Invalid value format"
        }

# must contain required keys
    if "temperature" not in value or "aqi" not in value:
        return {
            "status": "ERROR",
            "reason": "Missing temperature or aqi"
        }

# must be numeric
    try:
        float(value.get("temperature"))
        float(value.get("aqi"))
    except ValueError:
        return {
            "status": "ERROR",
            "reason": "Invalid numeric values"
        }
    if not signal.get("location") and not signal.get("city"):
        return {"status": "ERROR", "reason": "Missing location"}
    trace_id = signal.get("trace_id") or f"trace_{uuid.uuid4().hex[:8]}"
    return {
        "signal_id": signal.get("signal_id"),
        "status": "VALID",
        "confidence_score": signal.get("confidence_score", 0.5),
        "trace_id": trace_id,
        "reason": signal.get("reason", ""),
        "value": signal.get("value"),
        "timestamp": signal.get("timestamp"),
        "location": signal.get("location") or signal.get("city", "unknown"),
        "signal_type": signal.get("signal_type", "environment"),
    }


# -------------------------------------------------------
# INTERNAL: Logging
# -------------------------------------------------------
'''def log_data(filename: str, log_type: str, data: dict):
    """Append a JSON log entry to logs/<filename>. Never crashes."""
    try:
        entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": log_type,
            "data": data,
        }
        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception:
        pass'''


def log_data(filename: str, log_type: str, data: dict):
    """Store logs as proper JSON array (submission-friendly)."""
    try:
        filepath = f"logs/{filename}"

        entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": log_type,
            "data": data,
        }

        # Load existing logs
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    logs = json.load(f)
            except:
                logs = []
        else:
            logs = []

        logs.append(entry)

        # Write back
        with open(filepath, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception:
        pass


# -------------------------------------------------------
# ROUTE 1: Health Check
# -------------------------------------------------------
@app.get("/test")
def test():
    return {"status": "OK", "message": "NICAI Task 5 — engine active"}


# -------------------------------------------------------
# ROUTE 2: Validate (Phase 2 contract alignment)
# -------------------------------------------------------
@app.post("/validate")
def validate(signal: dict):
    """Validate a single signal. Returns VALID / ERROR / IGNORED."""
    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        if validation is None:
            return {"status": "IGNORED"}

        if validation.get("status") == "ERROR":
            return validation

        log_data("validation_logs.json", "VALIDATION", validation)
        return validation

    except Exception as e:
        return error_response(str(e))


# -------------------------------------------------------
# ROUTE 3: Pipeline (validate + engine)
# -------------------------------------------------------
@app.post("/pipeline")
def run_pipeline(signal: dict):
    """Full pipeline: validate -> SanskarEngine -> output."""
    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        if validation is None:
            return {"status": "IGNORED"}

        if validation.get("status") == "ERROR":
            return validation

        # FIXED: was checking ALLOW/FLAG — now correctly passes VALID
        #analytics = run_engine(validation)
        analytics = orchestrate_intelligence(signal)
        if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
            return analytics

        return {
            "signal_id": validation.get("signal_id"),
            "trace_id": validation.get("trace_id"),
            "risk_level": analytics.get("risk_level"),
            "anomaly_type": analytics.get("anomaly_type"),
            "explanation": analytics.get("explanation"),
            "temporal_context": analytics.get("temporal_context"),
            "spatial_context": analytics.get("spatial_context"),
            "confidence_score": analytics.get("confidence_score"),
            "recommendation_signal": analytics.get("recommendation_signal"),
        }

    except Exception as e:
        return error_response(str(e))


# -------------------------------------------------------
# ROUTE 4: /nicai/evaluate — PRIMARY INTEGRATION ENDPOINT
# Phase 4: this is the official NICAI evaluation route
# Flow: Samachar -> Validation -> SanskarEngine -> Output
# -------------------------------------------------------
@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):
    """
    Official NICAI evaluation endpoint.
    Accepts NICAI signal contract, returns NICAI output contract.
    """
    try:
        if not isinstance(signal, dict) or not signal:
            return error_response("Invalid or empty input")

        validation = validate_signal(signal)

        if validation is None:
            return {"status": "IGNORED"}

        if validation.get("status") == "ERROR":
            return validation

        #analytics = run_engine(validation)
        analytics = orchestrate_intelligence(signal)
        if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
            return analytics

        # NICAI output contract (Phase 3 — all 6 required fields)
        output = {
            "signal_id": validation.get("signal_id"),
            "trace_id": validation.get("trace_id"),
            "risk_level": analytics.get("risk_level"),
            "anomaly_type": analytics.get("anomaly_type"),
            "explanation": analytics.get("explanation"),
            "temporal_context": analytics.get("temporal_context"),
            "spatial_context": analytics.get("spatial_context"),
            "confidence_score": analytics.get("confidence_score"),
            "recommendation_signal": analytics.get("recommendation_signal"),
            # 🔥 ADD THESE (IMPORTANT)
            "region_insight": analytics.get("region_insight"),
            "spatial_risk": analytics.get("spatial_risk"),
            "domain_note": analytics.get("domain_note"),
        }

        log_data("anomaly_logs.json", "ANALYSIS", output)
        return output

    except Exception as e:
        return error_response(str(e))


# -------------------------------------------------------
# ROUTE 5: Batch run on CSV data
# -------------------------------------------------------
@app.get("/run")
def run_full_pipeline():
    """Batch-process first 50 signals from CSV datasets."""
    try:
        weather, aqi = load_data()
        if weather is None or aqi is None:
            return error_response("Data loading failed — check CSV files")

        signals = convert_to_signals(weather, aqi)

        gate = validate_basic_input(signals)
        if gate:
            return gate

        results = []

        for signal in signals[:50]:
            validation = validate_signal(signal)

            if validation is None:
                continue

            if validation.get("status") == "ERROR":
                continue

            #analytics = run_engine(validation)
            analytics = orchestrate_intelligence(signal)

            if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
                continue

            output = {
                "signal_id": str(signal.get("signal_id")),
                "trace_id": str(validation.get("trace_id")),
                "risk_level": str(analytics.get("risk_level", "LOW")),
                "anomaly_type": str(analytics.get("anomaly_type", "normal")),
                "explanation": str(analytics.get("explanation", "No issue")),
                "temporal_context": analytics.get("temporal_context"),
                "spatial_context": analytics.get("spatial_context"),
                "confidence_score": analytics.get("confidence_score"),
                "recommendation_signal": analytics.get("recommendation_signal"),
            }

            results.append(output)
            log_data("anomaly_logs.json", "ANALYSIS", output)

        # Pattern summary
        total = len(results)
        high = sum(1 for r in results if r.get("risk_level") == "HIGH")
        medium = sum(1 for r in results if r.get("risk_level") == "MEDIUM")
        low = sum(1 for r in results if r.get("risk_level") == "LOW")

        summary = {
            "pattern_id": "pattern_batch",
            "count": total,
            "type": "risk_distribution",
            "summary": f"HIGH: {high}, MEDIUM: {medium}, LOW: {low}",
        }

        log_data("pattern_logs.json", "PATTERN", summary)

        return {
            "total_processed": total,
            "summary": summary,
            "data": results,
        }

    except Exception as e:
        return error_response(str(e))


# -------------------------------------------------------
# ROUTE 6: Dashboard (Phase 5 — dashboard wiring)
# Shows: risk_level, anomaly_type, explanation, recommendation_signal
# No blank values — all fields guaranteed by integration_adapter
# -------------------------------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Live dashboard powered by SanskarEngine output."""
    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)
        results = []

        for signal in signals[:20]:
            validation = validate_signal(signal)

            if validation is None:
                continue

            if validation.get("status") == "ERROR":
                continue

            #analytics = run_engine(signal)
            analytics = orchestrate_intelligence(signal)
            if isinstance(analytics, dict) and analytics.get("status") == "ERROR":
                continue

            results.append({
                "signal_id": signal.get("signal_id"),
                "risk_level": analytics.get("risk_level", "LOW"),
                "anomaly_type": analytics.get("anomaly_type", "normal"),
                "explanation": analytics.get("explanation", "—"),
                "temporal_context": analytics.get("temporal_context", "STABLE"),
                "spatial_context": analytics.get("spatial_context", "—"),
                "confidence_score": analytics.get("confidence_score", 0.5),
                "recommendation_signal": analytics.get("recommendation_signal", "monitor"),
                "trace_id": validation.get("trace_id"),
            })

        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "data": results,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"<h1>Dashboard Error: {str(e)}</h1>")


# -------------------------------------------------------
# ROUTE 7: Action (Phase 6 — action flow check)
# Buttons: Escalate / Review / Assign
# Logs to action_logs.json with correct trace_id
# -------------------------------------------------------
@app.post("/action")
def trigger_action(data: dict):
    """
    Log an action from the dashboard (Escalate / Review / Assign).
    Updates action_logs.json with trace_id + action_type.
    """
    try:
        if not isinstance(data, dict) or not data:
            return error_response("Invalid or empty input")

        # Phase 6: correct trace_id mapping + context passed
        action_payload = {
            "trace_id": data.get("trace_id"),
            "action_type": data.get("action_type", "monitor"),
            "target_role": data.get("target_role", "authority"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": data.get("context", {}),
            "signal_id": data.get("signal_id"),
        }

        log_data("action_logs.json", "ACTION", action_payload)

        return {"status": "SUCCESS", "action": action_payload}

    except Exception as e:
        return error_response(str(e))
