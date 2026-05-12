from schemas import required_top_fields
from failure_handler import build_failure
import uuid

def generate_trace_id(signal):
    return f"trace_{uuid.uuid4().hex[:8]}"

def validate_output_schema(x):
    return True

# SAFE OPTIONAL IMPORTS
try:
    from bucket_emitter import emit_bucket_artifact
    from telemetry_emitter import emit_telemetry
except ImportError:
    def emit_bucket_artifact(x): pass
    def emit_telemetry(a, b): pass


def build_error(reason, trace_id=None, signal=None):
    return {
        "signal_id": signal.get("signal_id") if isinstance(signal, dict) else None,
        "status": "ERROR",
        "confidence_score": 0.0,
        "trace_id": trace_id,
        "reason": reason
    }


def validate_signal(signal):
    try:
        #if not isinstance(signal, dict):
            #return build_error("Invalid signal format")
        if not isinstance(signal, dict):
            failure = build_failure(
                "unknown",
                "VALIDATION",
                "Invalid signal format",
                "HIGH"
            )
            return build_error("Invalid signal format")
        trace_id = signal.get("trace_id") or generate_trace_id(signal)

        for field in required_top_fields:

            if field not in signal or signal.get(field) in [None, ""]:

                build_failure(
                    trace_id,
                    "VALIDATION",
                    f"Missing field: {field}",
                    "HIGH"
                )

                return build_error(
                    f"Missing field: {field}",
                    trace_id,
                    signal
                )
        value = signal.get("value")

        if not isinstance(value, dict):
            return build_error("Invalid value format", trace_id, signal)

        if "temperature" not in value or "aqi" not in value:
            return build_error("Missing temperature or aqi", trace_id, signal)

        result = {
            "signal_id": signal.get("signal_id"),
            "status": "VALID",
            "confidence_score": 0.9,
            "trace_id": trace_id,
            "reason": "Valid signal"
        }

        validate_output_schema(result)
        emit_bucket_artifact(
            "validation_logs.json",
            "VALIDATION",
            result
        )
        emit_telemetry(signal, result)

        return result

    #except Exception as e:
        #return build_error(str(e), None, signal)
    except Exception as e:

        failure = build_failure(
            signal.get("trace_id", "unknown")
            if isinstance(signal, dict)
            else "unknown",
            "VALIDATION",
            str(e),
            "HIGH"
        )

        return build_error(str(e), None, signal)

def validate_batch(signals):
    try:
        if not isinstance(signals, list):
            return {"status": "ERROR", "reason": "Input must be list", "trace_id": None}

        signals = sorted(signals, key=lambda x: x.get("signal_id", ""))
        results = [validate_signal(s) for s in signals]

        return {"results": results}

    except Exception as e:
        return {"status": "ERROR", "reason": str(e), "trace_id": None}


def get_validated_signals(signals):
    try:
        batch = validate_batch(signals)

        if batch.get("status") == "ERROR":
            return batch

        return [r for r in batch.get("results", []) if r.get("status") in ["VALID", "FLAG"]]

    except Exception as e:
        return {"status": "ERROR", "reason": str(e), "trace_id": None}
'''from schemas import required_top_fields

import uuid

def generate_trace_id(signal):
    return f"trace_{uuid.uuid4().hex[:8]}"
# -------------------------------
# SAFE OPTIONAL IMPORTS
# ------------------------------- 
try:
    from bucket_emitter import emit_bucket_artifact
    from telemetry_emitter import emit_telemetry
except ImportError:
    def emit_bucket_artifact(x): pass
    def emit_telemetry(a, b): pass


# -------------------------------
# STANDARD ERROR FORMAT (FIX)
# -------------------------------
def build_error(reason, trace_id=None, signal=None):
    return {
        "signal_id": signal.get("signal_id") if isinstance(signal, dict) else None,
        "status": "ERROR",
        "confidence_score": 0.0,
        "trace_id": trace_id,
        "reason": reason
    }


# -------------------------------
# VALIDATE SINGLE SIGNAL
# -------------------------------
def validate_signal(signal):

    try:
        # BASIC CHECK
        if not isinstance(signal, dict):
            return build_error("Invalid signal format")

        trace_id = generate_trace_id(signal)

        # REQUIRED FIELDS
        required_fields = ["signal_id", "value", "timestamp", "location"]
        for field in required_top_fields:
            if field not in signal or signal.get(field) in [None, ""]:
                return build_error(f"Missing field: {field}", trace_id, signal)

        # VALUE VALIDATION
        value = signal.get("value")

        if value is None:
            return build_error("Missing value", trace_id, signal)

        if not isinstance(value, dict):
            return build_error("Invalid value format", trace_id, signal)

        if "temperature" not in value or "aqi" not in value:
            return build_error("Missing temperature or aqi", trace_id, signal)

        # FINAL OUTPUT
        result = {
            "signal_id": signal.get("signal_id"),
            "status": "VALID",
            "confidence_score": 0.9,
            "trace_id": trace_id,
            "reason": "Valid signal"
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    except Exception as e:
        return build_error(str(e), None, signal)
        # -------------------------------
# 4️⃣ VALUE VALIDATION (NEW)
# -------------------------------
        value = signal.get("value")

        if value is None:
            return build_error("Missing value", trace_id, signal)

        if not isinstance(value, dict):
            return build_error("Invalid value format", trace_id, signal)

        # -------------------------------
        # 4️⃣ VALUE VALIDATION (NEW)
        # -------------------------------
        # OPTIONAL: check keys inside value
        if "temperature" not in value or "aqi" not in value:
            return build_error("Missing temperature or aqi", trace_id, signal)

# -------------------------------
# 5️⃣ FINAL STATUS (SIMPLE)       
# -------------------------------
        status = "VALID"
        confidence = 0.9
        reason = "Valid signal"

        # -------------------------------
        # FINAL OUTPUT
        # -------------------------------
        result = {
            "signal_id": signal.get("signal_id"),
            "status": status,
            "confidence_score": confidence,
            "trace_id": trace_id,
            "reason": reason
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    except Exception as e:
        return build_error(str(e), None, signal)


# -------------------------------
# VALIDATE BATCH
# -------------------------------
def validate_batch(signals):

    try:
        if not isinstance(signals, list):
            return {
                "status": "ERROR",
                "reason": "Input must be list",
                "trace_id": None
            }

        signals = sorted(signals, key=lambda x: x.get("signal_id", ""))

        results = [validate_signal(s) for s in signals]

        return {"results": results}

    except Exception as e:
        return {
            "status": "ERROR",
            "reason": str(e),
            "trace_id": None
        }


# -------------------------------
# FILTER VALID SIGNALS
# -------------------------------
def get_validated_signals(signals):

    try:
        batch = validate_batch(signals)

        if batch.get("status") == "ERROR":
            return batch

        return [
            r for r in batch.get("results", [])
            if r.get("status") in ["VALID", "FLAG"]
        ]

    except Exception as e:
        return {
            "status": "ERROR",
            "reason": str(e),
            "trace_id": None
        }
'''