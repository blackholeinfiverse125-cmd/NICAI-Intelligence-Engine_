from bucket_emitter import emit_bucket_artifact as log_data


def build_failure(
    trace_id,
    stage,
    reason,
    severity="MEDIUM"
):
    failure = {
        "trace_id": trace_id,
        "stage": stage,
        "reason": reason,
        "severity": severity,
        "status": "FAILED"
    }

    log_data(
        "failure_logs.json",
        "FAILURE",
        failure
    )

    return failure