from replay_corruption_simulator import (
    simulate_missing_stage,
    simulate_duplicate_stage,
    simulate_sequence_corruption
)

from telemetry_emitter import (
    generate_governance_metrics
)
from recovery_router import determine_recovery_action

from replay_divergence_checker import (
    detect_replay_divergence
)

trace_id = input("Enter trace_id: ")


mode = input(
    "Simulation mode (none/missing/duplicate/sequence): "
).strip().lower()

simulated_entries = None

if mode == "missing":

    simulated_entries = simulate_missing_stage(
        trace_id,
        "ACTION"
    )

elif mode == "duplicate":

    simulated_entries = simulate_duplicate_stage(
        trace_id,
        "ACTION"
    )

elif mode == "sequence":

    simulated_entries = simulate_sequence_corruption(
        trace_id
    )

result = detect_replay_divergence(
    trace_id,
    replay_entries=simulated_entries
)

print("\nDIVERGENCE RESULT\n")
print(result)

if result["divergence_detected"]:

    print("\nRECOVERY ACTIONS\n")

    for failure in result["issues"]:

        if isinstance(failure, dict):

            recovery = determine_recovery_action(
                failure
            )

            print({
                "failure": failure,
                "recovery": recovery
            })
    telemetry = generate_governance_metrics(
        result["issues"]
    )

    print("\nGOVERNANCE TELEMETRY\n")

    print(telemetry)