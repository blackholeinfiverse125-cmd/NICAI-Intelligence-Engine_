import json
import os

LOG_FILES = [
    "logs/ingestion_logs.json",
    "logs/tantra_logs.json",
    "logs/validation_logs.json",
    "logs/anomaly_logs.json",
    "logs/pattern_logs.json",
    "logs/contract_logs.json",
    "logs/action_logs.json",
    "logs/ttg_logs.json"
]
REQUIRED_STAGES = [
    "INGESTION",
    "TANTRA_PARTICIPATION",
    "VALIDATION",
    "ANALYSIS",
    "CLUSTER_ANALYSIS",
    "CONTRACT_VALIDATION",
    "ACTION",
    "TTG_CONSUME"
]


def load_logs(filepath):

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return []
    
def find_trace_entries(trace_id):

    collected = []

    for filepath in LOG_FILES:

        logs = load_logs(filepath)

        for entry in logs:

            entry_trace = (
            entry.get("trace_id")
            or entry.get("data", {}).get("trace_id")
            )

            if entry_trace == trace_id:
                collected.append(entry)
    #return collected
        # ---------------------------------
    # IMMUTABLE ORDER RECONSTRUCTION
    # ---------------------------------
    collected.sort(
        key=lambda x: x.get("sequence_id", 0)
    )

    return collected




def verify_replay(trace_id):

    entries = find_trace_entries(trace_id)
    sequence_ids = [
        entry.get("sequence_id")
        for entry in entries
        if entry.get("sequence_id") is not None
    ]

    ordered_correctly = (
        sequence_ids ==
        sorted(sequence_ids)
    )

    found_stages = [
        entry.get("type")
        for entry in entries
    ]

    missing = [
        stage
        for stage in REQUIRED_STAGES
        if stage not in found_stages
    ]

    return {
        "trace_id": trace_id,
        "found_stages": found_stages,
        "missing_stages": missing,
        "ordered_replay": ordered_correctly,
        "sequence_chain": sequence_ids,
        "replay_status": (
            "COMPLETE"
            if not missing
            else "INCOMPLETE"
        )
    }

if __name__ == "__main__":

    test_trace = input("Enter trace_id: ")

    replay_entries = find_trace_entries(test_trace)

    print("\nREPLAY ENTRIES\n")
    print(json.dumps(replay_entries, indent=2))

    summary = verify_replay(test_trace)

    print("\nREPLAY SUMMARY\n")
    print(json.dumps(summary, indent=2))