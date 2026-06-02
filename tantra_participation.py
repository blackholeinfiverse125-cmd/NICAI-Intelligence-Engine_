from bucket_emitter import emit_bucket_artifact


def emit_tantra_participation(output: dict):

    participation = {
        "trace_id": output.get("trace_id"),
        "consumer": "TANTRA",
        "ack_status": "ACCEPTED",
        "participation_type": "DOWNSTREAM_CONTRACT"
    }

    emit_bucket_artifact(
        "tantra_logs.json",
        "TANTRA_PARTICIPATION",
        participation
    )

    return participation