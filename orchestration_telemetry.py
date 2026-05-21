from datetime import datetime, timezone
from bucket_emitter import emit_bucket_artifact

def emit_orchestration_event(
    trace_id,
    stage,
    status,
    metadata=None,
    latency_ms=None
):

    telemetry_event = {
        "trace_id": trace_id,
        "stage": stage,
        "status": status,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "latency_ms": latency_ms,
        "metadata": metadata or {}
    }

    

    emit_bucket_artifact(
        "orchestration_logs.json",
        "ORCHESTRATION",
        telemetry_event
    )

    return telemetry_event