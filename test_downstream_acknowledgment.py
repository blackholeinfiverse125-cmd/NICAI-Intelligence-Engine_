from downstream_acknowledger import (
    validate_downstream_acknowledgment,
    detect_orphan_acknowledgment
)

# ---------------------------------
# VALID ACKNOWLEDGMENT
# ---------------------------------

valid_ack = {
    "trace_id": "trace_demo",
    "ack_status": "ACCEPTED",
    "consumer": "TANTRA"
}

valid_result = validate_downstream_acknowledgment(
    "trace_demo",
    valid_ack
)

print("\nVALID ACKNOWLEDGMENT\n")

print(valid_result)

# ---------------------------------
# TRACE MISMATCH
# ---------------------------------

trace_mismatch_ack = {
    "trace_id": "wrong_trace",
    "ack_status": "ACCEPTED",
    "consumer": "TANTRA"
}

trace_result = validate_downstream_acknowledgment(
    "trace_demo",
    trace_mismatch_ack
)

print("\nTRACE MISMATCH RESULT\n")

print(trace_result)

# ---------------------------------
# SCHEMA FAILURE
# ---------------------------------

invalid_schema_ack = {
    "trace_id": "trace_demo"
}

schema_result = validate_downstream_acknowledgment(
    "trace_demo",
    invalid_schema_ack
)

print("\nSCHEMA FAILURE RESULT\n")

print(schema_result)

# ---------------------------------
# ORPHAN ACKNOWLEDGMENT
# ---------------------------------

known_traces = [
    "trace_a",
    "trace_b"
]

orphan_result = detect_orphan_acknowledgment(
    "trace_unknown",
    known_traces
)

print("\nORPHAN ACKNOWLEDGMENT RESULT\n")

print(orphan_result)