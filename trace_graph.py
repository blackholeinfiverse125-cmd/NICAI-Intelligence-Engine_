import json
import os

LOG_DIR = "logs"

LOG_FILES = [
    "validation_logs.json",
    "anomaly_logs.json",
    "contract_logs.json",
    "action_logs.json",
    "failure_logs.json"
]


def load_logs():
    all_logs = []

    for file in LOG_FILES:
        path = os.path.join(LOG_DIR, file)

        if not os.path.exists(path):
            continue

        try:
            with open(path, "r") as f:
                data = json.load(f)

                if isinstance(data, list):
                    all_logs.extend(data)

        except Exception:
            continue

    return all_logs


def build_trace_graph(trace_id):
    logs = load_logs()

    matched = [
        log for log in logs
        if log.get("trace_id") == trace_id
    ]

    matched.sort(key=lambda x: x.get("timestamp", ""))

    graph = []

    for item in matched:
        graph.append({
            "timestamp": item.get("timestamp"),
            "type": item.get("type"),
            "trace_id": item.get("trace_id")
        })

    return graph


if __name__ == "__main__":
    trace_id = input("Enter trace_id: ")

    graph = build_trace_graph(trace_id)

    print("\nTRACE EXECUTION FLOW\n")

    for step in graph:
        print(
            f"{step['timestamp']}  -->  {step['type']}"
        )