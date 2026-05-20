from lineage_exporter import (
    export_replay_lineage
)

trace_id = input(
    "Enter trace_id: "
)

result = export_replay_lineage(
    trace_id
)

print("\nLINEAGE EXPORT RESULT\n")

print(result)

print("\nEXPORT COMPLETE\n")

print(
    "Replay-safe lineage exported successfully."
)