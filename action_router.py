from bucket_emitter import emit_bucket_artifact as log_data

def route_action(output: dict) -> dict:
    """
    Maps NICAI output → real execution action
    """

    risk = output.get("risk_level", "LOW")

    if risk == "HIGH":
        action = "RECOMMEND_ESCALATION_REVIEW"
    elif risk == "MEDIUM":
        action = "RECOMMEND_ENVIRONMENTAL_REVIEW"
    else:
        action = "CONTINUE_MONITORING"

    result = {
        "trace_id": output.get("trace_id", "unknown"),
        "action": action,
        "status": "EMITTED"
    }
    log_data(
        "action_logs.json",
        "ACTION",
        result
    )
    return result