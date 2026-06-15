# DEMO_EXECUTION_SPEC.md

## Purpose

This document defines the single authoritative execution path for the NICAI Demo Convergence Sprint.

The objective is to eliminate ambiguity and ensure every reviewer executes the same deterministic workflow.

---

# Canonical Demo Route

GET /run

This is the only approved execution route for demonstration and validation.

All other routes are supporting routes and are not considered authoritative for demo execution.

---

# Non-Canonical Routes

| Route           | Purpose                    |
| --------------- | -------------------------- |
| /test           | Health Check               |
| /validate       | Validation Testing         |
| /pipeline       | Single Signal Intelligence |
| /nicai/evaluate | API Evaluation Endpoint    |
| /dashboard      | Visualization Surface      |
| /action         | Manual Operator Action     |

These routes may be used for debugging, validation, or visualization but are not the official demo path.

---

# Authoritative Execution Chain

Dataset
→ Validation
→ Intelligence
→ Context Fusion
→ Cluster Analysis
→ Contract Validation
→ Action Routing
→ Bucket Persistence
→ TANTRA Participation
→ TTG Consumption
→ Replay Validation
→ Dashboard Visibility

---

# Core Execution Files

main.py

integration_orchestrator.py

cluster_intelligence.py

contract_validator.py

action_router.py

bucket_emitter.py

replay_engine.py

tantra_participation.py

ttg_simulation.py

---

# Demo Startup Procedure

Step 1

Start FastAPI server:

uvicorn main:app --reload

Step 2

Verify service health:

GET /test

Expected:

{
"status": "OK"
}

Step 3

Execute canonical route:

GET /run

Expected:

* Signals processed
* Validation completed
* Intelligence completed
* Cluster analysis completed
* Contract validation completed
* Action emitted
* TANTRA participation emitted
* TTG consumption emitted

---

# Expected Persistence Artifacts

logs/ingestion_logs.json

logs/validation_logs.json

logs/anomaly_logs.json

logs/pattern_logs.json

logs/contract_logs.json

logs/action_logs.json

logs/tantra_logs.json

logs/ttg_logs.json

---

# Replay Validation

After canonical execution:

Run replay validation using:

replay_engine.py

Expected:

Replay chain reconstructed successfully.

No missing stages for valid execution.

---

# Dashboard Verification

Open:

/dashboard

Expected visibility:

* Signal Analysis
* Execution Trace
* Consumer Registry
* Execution Correlation
* Consumer Health
* Replay Integrity
* Operational Status

---

# Success Criteria

The demo is considered successful when:

1. /run executes successfully.
2. Logs are persisted.
3. Contract validation succeeds.
4. TANTRA participation succeeds.
5. TTG consumption succeeds.
6. Replay reconstruction succeeds.
7. Dashboard displays execution output.
8. Trace continuity is preserved.

---

# Canonical System Statement

NICAI shall be demonstrated using a single authoritative execution route:

GET /run

No alternative route shall be used as the official demonstration path.
