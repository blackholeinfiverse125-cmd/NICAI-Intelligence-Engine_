"""
run_demo_full.py — NICAI Full System Demo (Task 5)
Sanskar Pandey

SINGLE COMMAND: python run_demo_full.py

Verifies all 7 pipeline stages:
  1. Dataset ingestion
  2. Signal creation
  3. Validation
  4. SanskarEngine execution
  5. Dashboard display (instruction)
  6. Action click simulation
  7. Logs updated
"""

import json
import os
from datetime import datetime, timezone

from samachar_input_adapter import load_data, convert_to_signals
from validator import validate_signal
from sanskar_engine import analyze_patterns
from integration_adapter import run_engine
from error_handler import error_response, validate_basic_input

# Ensure required folders
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)


def log_data(filename: str, log_type: str, data: dict):
    """Safe append logger."""
    try:
        entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": log_type,
            "data": data,
        }
        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception:
        pass


def simulate_action(trace_id: str, action_type: str):
    """Simulate dashboard button click -> writes to action_logs.json."""
    payload = {
        "trace_id": trace_id,
        "action_type": action_type,
        "target_role": "authority",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "context": {"demo": True},
    }
    log_data("action_logs.json", "ACTION", payload)
    return payload


def run_demo():
    print("\n==============================")
    print(" NICAI FULL SYSTEM DEMO START")
    print("==============================\n")

    # ------------------------------------------------
    # STEP 1: Dataset ingestion
    # ------------------------------------------------
    print("STEP 1 — Loading datasets...")
    weather, aqi = load_data()

    if weather is None or aqi is None:
        print(json.dumps(error_response("Dataset loading failed"), indent=2))
        return

    print(f"  weather rows: {len(weather)}")
    print(f"  aqi rows:     {len(aqi)}\n")

    # ------------------------------------------------
    # STEP 2: Signal creation
    # ------------------------------------------------
    print("STEP 2 — Converting to signals...")
    signals = convert_to_signals(weather, aqi)

    gate = validate_basic_input(signals)
    if gate:
        print(json.dumps(gate, indent=2))
        return

    print(f"  Total signals created: {len(signals)}\n")

    # ------------------------------------------------
    # STEP 3 + 4: Validation + SanskarEngine execution
    # ------------------------------------------------
    print("------------------------------------")
    print("STEP 3+4 — Validation + Intelligence")
    print("------------------------------------\n")

    processed_outputs = []
    low = medium = high = 0
    errors = 0

    for signal in signals[:20]:
        if not isinstance(signal, dict):
            continue

        # STEP 3: Validation
        validation = validate_signal(signal)
        if validation is None:
            continue
        if validation.get("status") == "ERROR":
            errors += 1
            continue

        log_data("validation_logs.json", "VALIDATION", validation)

        # STEP 4: SanskarEngine execution
        analysis = run_engine(signal)

        if not isinstance(analysis, dict) or analysis.get("status") == "ERROR":
            errors += 1
            continue

        output = {
            "signal_id": signal.get("signal_id"),
            "trace_id": validation.get("trace_id"),
            "risk_level": analysis.get("risk_level", "LOW"),
            "anomaly_type": analysis.get("anomaly_type", "normal"),
            "explanation": analysis.get("explanation", "—"),
            "temporal_context": analysis.get("temporal_context"),
            "spatial_context": analysis.get("spatial_context"),
            "confidence_score": analysis.get("confidence_score"),
            "recommendation_signal": analysis.get("recommendation_signal"),
        }

        processed_outputs.append(output)
        log_data("anomaly_logs.json", "ANALYSIS", output)

        rl = output["risk_level"]
        if rl == "LOW":
            low += 1
        elif rl == "MEDIUM":
            medium += 1
        elif rl == "HIGH":
            high += 1

    print("  Sample output (first signal):")
    if processed_outputs:
        print(json.dumps(processed_outputs[0], indent=2, default=str))

    print(f"\n  SUMMARY: LOW={low}, MEDIUM={medium}, HIGH={high}, ERRORS={errors}\n")

    # ------------------------------------------------
    # STEP 5: Dashboard display
    # ------------------------------------------------
    print("------------------------------------")
    print("STEP 5 — Dashboard")
    print("------------------------------------")
    print("  Start server: uvicorn main:app --reload")
    print("  Open:         http://127.0.0.1:8000/dashboard")
    print("  API docs:     http://127.0.0.1:8000/docs\n")

    # ------------------------------------------------
    # STEP 6: Action click simulation
    # ------------------------------------------------
    print("------------------------------------")
    print("STEP 6 — Action Click Simulation")
    print("------------------------------------")

    if processed_outputs:
        sample = processed_outputs[0]
        action = simulate_action(
            trace_id=sample.get("trace_id", "trace_demo"),
            action_type=sample.get("recommendation_signal", "monitor"),
        )
        print("  Action logged:")
        print(json.dumps(action, indent=2))
    else:
        print("  No processed outputs — skipping action simulation\n")

    # ------------------------------------------------
    # STEP 7: Pattern detection + logs verification
    # ------------------------------------------------
    print("\n------------------------------------")
    print("STEP 7 — Pattern Detection + Log Verification")
    print("------------------------------------")

    if processed_outputs:
        pattern = analyze_patterns(processed_outputs)
    else:
        pattern = {"pattern_type": "NO_PATTERN", "severity_trend": "NONE", "summary": "No data"}

    log_data("pattern_logs.json", "PATTERN", pattern)

    print("  Pattern:")
    print(json.dumps(pattern, indent=2, default=str))

    print("\n  Log files updated:")
    for f in ["validation_logs.json", "anomaly_logs.json", "action_logs.json", "pattern_logs.json"]:
        path = f"logs/{f}"
        try:
            size = os.path.getsize(path)
            print(f"    logs/{f} ({size} bytes)")
        except Exception:
            print(f"    logs/{f} — not found")

    print("\n================================")
    print(" NICAI DEMO COMPLETE")
    print("================================\n")


if __name__ == "__main__":
    run_demo()
