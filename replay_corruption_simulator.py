import json

from replay_engine import (
    find_trace_entries
)


def simulate_missing_stage(
    trace_id,
    stage_to_remove
):

    entries = find_trace_entries(trace_id)

    corrupted = [
        entry
        for entry in entries
        if entry.get("type") != stage_to_remove
    ]

    return corrupted

def simulate_duplicate_stage(
    trace_id,
    stage_to_duplicate
):

    entries = find_trace_entries(trace_id)

    duplicated = []

    for entry in entries:

        duplicated.append(entry)

        if entry.get("type") == stage_to_duplicate:

            duplicated.append(entry)

    return duplicated

def simulate_sequence_corruption(
    trace_id
):

    entries = find_trace_entries(trace_id)

    corrupted = list(entries)

    if len(corrupted) >= 2:

        corrupted[0]["sequence_id"] = (
            corrupted[-1]["sequence_id"] + 100
        )

    return corrupted