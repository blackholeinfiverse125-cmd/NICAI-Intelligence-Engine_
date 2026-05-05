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

    return {
        "trace_id": output.get("trace_id"),
        "action": action,
        "status": "TRIGGERED"
    }