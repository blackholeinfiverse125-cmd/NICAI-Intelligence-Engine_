REQUIRED_ACK_FIELDS = [
    "trace_id",
    "ack_status",
    "consumer"
]


def validate_downstream_acknowledgment(
    original_trace_id,
    acknowledgment
):

    # ---------------------------------
    # TYPE VALIDATION
    # ---------------------------------
    if not isinstance(acknowledgment, dict):

        return {
            "ack_valid": False,
            "reason": "Invalid acknowledgment structure"
        }

    # ---------------------------------
    # REQUIRED FIELD VALIDATION
    # ---------------------------------
    for field in REQUIRED_ACK_FIELDS:

        if field not in acknowledgment:

            return {
                "ack_valid": False,
                "reason": f"Missing acknowledgment field: {field}"
            }

    # ---------------------------------
    # TRACE CONTINUITY VALIDATION
    # ---------------------------------
    if acknowledgment.get("trace_id") != original_trace_id:

        return {
            "ack_valid": False,
            "reason": "TRACE_MISMATCH"
        }

    # ---------------------------------
    # ACK STATUS VALIDATION
    # ---------------------------------
    if acknowledgment.get("ack_status") not in [
        "ACCEPTED",
        "REJECTED"
    ]:

        return {
            "ack_valid": False,
            "reason": "Invalid acknowledgment status"
        }

    # ---------------------------------
    # FINAL SUCCESS
    # ---------------------------------
    return {
        "ack_valid": True,
        "acknowledgment": acknowledgment
    }
def detect_orphan_acknowledgment(
    trace_id,
    known_traces
):

    if trace_id not in known_traces:

        return {
            "orphan_detected": True,
            "reason": "ORPHAN_ACKNOWLEDGMENT"
        }

    return {
        "orphan_detected": False
    }