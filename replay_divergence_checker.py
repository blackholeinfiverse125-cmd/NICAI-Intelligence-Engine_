from failure_matrix import FAILURE_MATRIX
from replay_engine import (
    find_trace_entries,
    REQUIRED_STAGES
)


def detect_replay_divergence(
    trace_id,
    replay_entries=None
):

    entries = (
        replay_entries
        if replay_entries is not None
        else find_trace_entries(trace_id)
    )

    divergence = []

    # ---------------------------------
    # CHECK 1 — EMPTY REPLAY
    # ---------------------------------
    if not entries:

        '''divergence.append(
            "No replay entries found"
        )'''
        divergence.append({
            "failure_type": "EMPTY_REPLAY",
            "metadata": FAILURE_MATRIX["EMPTY_REPLAY"]
        })

        return {
            "trace_id": trace_id,
            "divergence_detected": True,
            "issues": divergence
        }

    # ---------------------------------
    # CHECK 2 — MISSING STAGES
    # ---------------------------------
    found_stages = [
        entry.get("type")
        for entry in entries
    ]

    for stage in REQUIRED_STAGES:

        if stage not in found_stages:

            '''divergence.append(
                f"Missing stage: {stage}"
            )'''
            divergence.append({
                "failure_type": "MISSING_STAGE",
                "failed_stage": stage,
                "metadata": FAILURE_MATRIX["MISSING_STAGE"]
            })

    # ---------------------------------
    # CHECK 3 — ORDER VALIDATION
    # ---------------------------------
    sequence_ids = [
        entry.get("sequence_id")
        for entry in entries
        if entry.get("sequence_id") is not None
    ]

    if sequence_ids != sorted(sequence_ids):

        '''divergence.append(
            "Sequence ordering corruption detected"
        )'''
        divergence.append({
            "failure_type": "SEQUENCE_CORRUPTION",
            "metadata": FAILURE_MATRIX["SEQUENCE_CORRUPTION"]
        })

    # ---------------------------------
    # CHECK 4 — DUPLICATE STAGES
    # ---------------------------------
    for stage in REQUIRED_STAGES:

        if found_stages.count(stage) > 1:

            '''divergence.append(
                f"Duplicate stage detected: {stage}"
            )'''
            divergence.append({
                "failure_type": "DUPLICATE_STAGE",
                "failed_stage": stage,
                "metadata": FAILURE_MATRIX["DUPLICATE_STAGE"]
            })
    # ---------------------------------
    # FINAL RESULT
    # ---------------------------------
    return {
        "trace_id": trace_id,
        "divergence_detected": (
            len(divergence) > 0
        ),
        "issues": divergence if divergence else [
            "Replay integrity verified"
        ]
    }