import json
import os
from datetime import datetime, timezone
from sequence_manager import get_next_sequence_id
LOG_DIR = "logs"


def emit_bucket_artifact(filename: str, event_type: str, data: dict):
    """
    Append structured deterministic logs safely.
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    filepath = os.path.join(LOG_DIR, filename)

    log_entry = {
        "sequence_id": get_next_sequence_id(),
        "trace_id": data.get("trace_id", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "data": dict(data)
    }

    try:
        # Create file if missing
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)

        # Read existing logs
        with open(filepath, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

        # Append new log
        logs.append(log_entry)

        # Save updated logs
        with open(filepath, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:

        failure_log = {
            "timestamp": datetime.now(
            timezone.utc
            ).isoformat(),

            "failed_file": filename,

            "event_type": event_type,

            "error": str(e)
        }

        try:

            os.makedirs(
                LOG_DIR,
                exist_ok=True
            )

            failure_path = os.path.join(
                LOG_DIR,
                "bucket_failures.json"
            )

            if os.path.exists(failure_path):

                with open(
                    failure_path,
                    "r"
                ) as f:

                    try:
                        failures = json.load(f)

                    except:
                        failures = []

            else:

                failures = []

            failures.append(
                failure_log
            )

            with open(
                failure_path,
                "w"
            ) as f:

                json.dump(
                    failures,
                    f,
                    indent=2
                )

        except Exception:
            pass

        print(
            f"[BUCKET ERROR] {e}"
        )