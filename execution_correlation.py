import json

from consumer_registry import (
    lookup_consumer
)


def build_execution_correlation(
    execution_id,
    trace_id,
    contract_id,
    consumer_name
):

    consumer = lookup_consumer(
        consumer_name
    )

    if consumer is None:

        return {
            "correlation_status": "FAILED",
            "reason": "UNKNOWN_CONSUMER"
        }

    return {

        "execution_id": execution_id,

        "trace_id": trace_id,

        "contract_id": contract_id,

        "consumer_id":
            consumer.get("consumer_id"),

        "consumer_name":
            consumer.get("consumer_name"),

        "correlation_status":
            "COMPLETE"
    }


def export_execution_correlation(
    payload,
    filename="execution_correlation.json"
):

    with open(
        filename,
        "w"
    ) as f:

        json.dump(
            payload,
            f,
            indent=2
        )

    return filename