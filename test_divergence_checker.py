from telemetry_emitter import (
    generate_governance_metrics
)
from recovery_router import determine_recovery_action

from replay_divergence_checker import (
    detect_replay_divergence
)

trace_id = input("Enter trace_id: ")

result = detect_replay_divergence(trace_id)

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