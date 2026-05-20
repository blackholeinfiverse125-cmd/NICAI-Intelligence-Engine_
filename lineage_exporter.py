import json

from replay_engine import (
    find_trace_entries
)


def export_replay_lineage(
    trace_id,
    export_file="exported_lineage.json"
):

    entries = find_trace_entries(trace_id)

    export_payload = {
        "trace_id": trace_id,
        "replay_safe": True,
        "total_events": len(entries),
        "lineage": entries
    }

    with open(export_file, "w") as f:

        json.dump(
            export_payload,
            f,
            indent=2
        )

    return export_payload