import os
import json

SEQUENCE_FILE = "logs/sequence_state.json"


def get_next_sequence_id():

    os.makedirs("logs", exist_ok=True)

    # -----------------------------
    # INITIALIZE STATE
    # -----------------------------
    if not os.path.exists(SEQUENCE_FILE):

        with open(SEQUENCE_FILE, "w") as f:
            json.dump({"last_sequence": 0}, f)

    # -----------------------------
    # LOAD CURRENT STATE
    # -----------------------------
    with open(SEQUENCE_FILE, "r") as f:
        state = json.load(f)

    current = state.get("last_sequence", 0)

    next_sequence = current + 1

    # -----------------------------
    # SAVE UPDATED STATE
    # -----------------------------
    with open(SEQUENCE_FILE, "w") as f:
        json.dump(
            {"last_sequence": next_sequence},
            f,
            indent=2
        )

    return next_sequence