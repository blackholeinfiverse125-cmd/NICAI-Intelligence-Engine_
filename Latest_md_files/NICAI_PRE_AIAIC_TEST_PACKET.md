# NICAI — Pre-AIAIC Operational Test Packet

## Purpose

This packet validates that NICAI executes as one bounded deterministic orchestration system.

This test packet is intended for:

- Vinayak Tiwari
- operational reviewers
- replay auditors
- governance testers
- AIAIC transition engineers

Estimated execution time:

5–10 minutes

---

# Test Objective

Validate:

- API execution
- replay reconstruction
- contract enforcement
- trace continuity
- action routing
- lineage persistence
- replay divergence detection
- dashboard visibility

---

# Environment Setup

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start FastAPI server

```bash
uvicorn main:app --reload
```

Expected server:

```text
http://127.0.0.1:8000
```

---

# Test 1 — Health Check

## Route

```text
GET /test
```

## Expected Result

```json
{
  "status": "OK",
  "message": "NICAI Task 5 — engine active"
}
```

## Validation Goal

Confirm FastAPI orchestration operational.

---

# Test 2 — Canonical Execution Spine

## Route

```text
GET /run
```

## Expected Result

Response should contain:

- cluster_result
- action
- total_signals

Expected orchestration stages:

- VALIDATION
- ANALYSIS
- CLUSTER_ANALYSIS
- CONTRACT_VALIDATION
- ACTION

## Validation Goal

Confirm deterministic governance-aware orchestration execution.

---

# Test 3 — Replay Reconstruction

## Command

```bash
python replay_engine.py
```

## Input

Provide a valid trace_id from /run execution.

## Expected Result

Replay reconstruction should contain:

- VALIDATION
- ANALYSIS
- CLUSTER_ANALYSIS
- CONTRACT_VALIDATION
- ACTION

Replay status:

```text
COMPLETE
```

## Validation Goal

Confirm deterministic replay reconstruction.

---

# Test 4 — Lineage Export Validation

## Command

```bash
python test_lineage_export.py
```

## Expected Result

Export should contain:

- immutable sequence IDs
- ordered orchestration stages
- replay-safe lineage continuity
- trace continuity

## Validation Goal

Confirm lineage export reconstruction.

---

# Test 5 — Contract Enforcement Validation

## Command

```bash
python test_downstream_acknowledgment.py
```

## Expected Result

System should validate:

- valid acknowledgment
- malformed acknowledgment rejection
- trace mismatch rejection
- orphan acknowledgment detection

## Validation Goal

Confirm downstream governance enforcement.

---

# Test 6 — Replay Divergence Detection

## Command

```bash
python test_divergence_checker.py
```

## Expected Result

System should detect:

- duplicate stages
- replay divergence
- missing stages
- orphan events

## Validation Goal

Confirm replay integrity enforcement.

---

# Test 7 — Dashboard Validation

## Route

```text
GET /dashboard
```

## Expected Result

Dashboard should display:

- risk_level
- anomaly_type
- explanation
- recommendation_signal
- trace_id

## Validation Goal

Confirm visualization layer operational.

---

# Replay Artifact Validation

Expected replay artifacts:

```text
logs/
```

Expected files:

- validation_logs.json
- anomaly_logs.json
- pattern_logs.json
- contract_logs.json
- action_logs.json
- failure_logs.json

---

# Governance Validation Checklist

| Capability | Expected Result |
|---|---|
| deterministic replay | PASS |
| immutable sequencing | PASS |
| contract enforcement | PASS |
| trace continuity | PASS |
| bounded action routing | PASS |
| replay divergence detection | PASS |
| lineage persistence | PASS |
| governance-safe orchestration | PASS |

---

# Operational Constraints

NICAI intentionally restricts execution to:

- recommendation emission
- escalation routing
- governance-safe bounded orchestration

NICAI does NOT autonomously execute real-world interventions.

---

# Final Validation Standard

NICAI should emerge from testing as:

- replay-safe
- governance-aware
- operationally bounded
- deterministically reconstructable
- integration coherent

Expected operational state:

```text
OPERATIONALLY_RESILIENT
```