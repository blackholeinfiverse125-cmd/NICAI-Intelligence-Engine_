from bucket_emitter import emit_bucket_artifact


def emit_ttg_consume(participation: dict):

    ttg_event = {
        "trace_id": participation.get("trace_id"),
        "consumer": "TTG",
        "simulation_pack": "RUDRA_ATHARVA",
        "consume_status": "CONSUMED"
    }

    emit_bucket_artifact(
        "ttg_logs.json",
        "TTG_CONSUME",
        ttg_event
    )

    return ttg_event