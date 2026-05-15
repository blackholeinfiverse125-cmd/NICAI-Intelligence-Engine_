def determine_recovery_action(failure):

    failure_type = failure.get("failure_type")

    metadata = failure.get("metadata", {})

    severity = metadata.get("severity")

    recoverable = metadata.get("recoverable")

    # ---------------------------------
    # HARD FAILURE ESCALATION
    # ---------------------------------
    if severity == "HIGH" and not recoverable:

        return {
            "recovery_action": "ESCALATE",
            "orchestration_status": "FROZEN"
        }

    # ---------------------------------
    # SAFE RETRY
    # ---------------------------------
    if severity == "MEDIUM" and recoverable:

        return {
            "recovery_action": "RETRY",
            "orchestration_status": "ACTIVE"
        }

    # ---------------------------------
    # LOW-RISK CONTINUE
    # ---------------------------------
    if severity == "LOW":

        return {
            "recovery_action": "CONTINUE",
            "orchestration_status": "ACTIVE"
        }

    # ---------------------------------
    # DEFAULT SAFETY
    # ---------------------------------
    return {
        "recovery_action": "MANUAL_REVIEW",
        "orchestration_status": "RESTRICTED"
    }