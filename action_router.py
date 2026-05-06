from bucket_emitter import emit_bucket_artifact as log_data

def route_action(output: dict) -> dict:
    """
    Maps NICAI output → real execution action
    """

    risk = output.get("risk_level", "LOW")

    if risk == "HIGH":
        action = "ESCALATE_TO_AUTHORITY"
    elif risk == "MEDIUM":
        action = "SEND_FOR_REVIEW"
    else:
        action = "MONITOR"

    result = {
        "trace_id": output.get("trace_id", "unknown"),
        "action": action,
        "status": "TRIGGERED"
    }
    log_data({
        "type": "ACTION",
        "data": result
    })
    return result