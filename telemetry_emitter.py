def emit_telemetry(event_type, payload):

    telemetry_event = {
        "event_type": event_type,
        "payload": payload
    }

    print("\nTELEMETRY EVENT\n")

    print(telemetry_event)

    return telemetry_event

from collections import Counter


def generate_governance_metrics(failures):

    metrics = {
        "total_failures": 0,
        "severity_breakdown": {},
        "category_breakdown": {},
        "recoverable_failures": 0,
        "non_recoverable_failures": 0
    }



    severity_counter = Counter()

    category_counter = Counter()

    for failure in failures:

        if not isinstance(failure, dict):
            continue

        metadata = failure.get(
            "metadata",
            {}
        )

        severity = metadata.get(
            "severity",
            "UNKNOWN"
        )

        category = metadata.get(
            "category",
            "UNKNOWN"
        )

        recoverable = metadata.get(
            "recoverable",
            False
        )

        severity_counter[severity] += 1

        category_counter[category] += 1

        metrics["total_failures"] += 1

        if recoverable:
            metrics["recoverable_failures"] += 1
        else:
            metrics["non_recoverable_failures"] += 1

    metrics["severity_breakdown"] = dict(
        severity_counter
    )

    metrics["category_breakdown"] = dict(
        category_counter
    )

    return metrics