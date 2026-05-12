ALLOWED_RISK_LEVELS = ["LOW", "MEDIUM", "HIGH"]

ALLOWED_RECOMMENDATIONS = [
    "monitor",
    "requires_review",
    "eligible_for_escalation"
]

ALLOWED_TEMPORAL = [
    "RISING",
    "STABLE",
    "FALLING",
    "CLUSTERED"
]

REQUIRED_FIELDS = [
    "trace_id",
    "risk_level",
    "anomaly_type",
    "explanation",
    "temporal_context",
    "spatial_context",
    "confidence",
    "recommendation_signal"
]


def validate_contract(output: dict) -> dict:

    errors = []

    # -----------------------------
    # TYPE CHECK
    # -----------------------------
    if not isinstance(output, dict):
        return {
            "contract_status": "INVALID",
            "errors": ["Output is not a dictionary"]
        }

    # -----------------------------
    # REQUIRED FIELD CHECK
    # -----------------------------
    for field in REQUIRED_FIELDS:
        if field not in output:
            errors.append(f"Missing field: {field}")

    
    # -----------------------------
    # ENUM VALIDATION
    # -----------------------------
    if output.get("risk_level") not in ALLOWED_RISK_LEVELS:
        errors.append("Invalid risk_level")

    if output.get("recommendation_signal") not in ALLOWED_RECOMMENDATIONS:
        errors.append("Invalid recommendation_signal")

    if output.get("temporal_context") not in ALLOWED_TEMPORAL:
        errors.append("Invalid temporal_context")

    # -----------------------------
    # CONFIDENCE VALIDATION
    # -----------------------------
    confidence = output.get("confidence")

    if not isinstance(confidence, (int, float)):
        errors.append("Confidence must be numeric")

    elif confidence < 0 or confidence > 1:
        errors.append("Confidence out of range")

    # -----------------------------
    # EXPLANATION VALIDATION
    # -----------------------------
    if not isinstance(output.get("explanation"), str):
        errors.append("Explanation must be string")

    # -----------------------------
    # FINAL RESULT
    # -----------------------------
    return {
        "trace_id": output.get("trace_id", "unknown"),
        "contract_status": "VALID" if not errors else "INVALID",
        "errors": errors
    }
    