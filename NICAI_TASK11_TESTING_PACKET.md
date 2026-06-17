# NICAI TASK 11 TESTING PACKET

## Purpose

Validate operational readiness of the NICAI Demo Convergence System using the BHIV Universal Testing Protocol.

Expected execution time:

5–10 minutes.

---

# Test 1 — Basic Execution

## Objective

Verify complete deterministic execution.

## Steps

1. Start FastAPI server.
2. Open:

GET /run

## Expected Result

System executes:

INGESTION
→ VALIDATION
→ ANALYSIS
→ CLUSTER_ANALYSIS
→ CONTRACT_VALIDATION
→ ACTION
→ TANTRA_PARTICIPATION
→ TTG_CONSUME

## Pass Criteria

* No exceptions
* Cluster result returned
* Action emitted
* TANTRA accepted
* TTG consumed

PASS / FAIL: ______

---

# Test 2 — Route Validation

## Routes

GET /test
POST /validate
POST /nicai/evaluate
GET /run
GET /dashboard

## Pass Criteria

All routes return expected responses.

PASS / FAIL: ______

---

# Test 3 — Contract Validation

## Objective

Verify governance enforcement.

## Procedure

Inject:

cluster_output["risk_level"] = "INVALID"

Run:

GET /run

## Expected

Contract validation returns INVALID.

Execution stops before:

* ACTION
* TANTRA
* TTG

PASS / FAIL: ______

---

# Test 4 — Replay Validation

## Procedure

Run:

python replay_engine.py

Provide valid trace_id.

## Expected

Replay Status:

COMPLETE

No missing stages.

PASS / FAIL: ______

---

# Test 5 — Trace Validation

## Objective

Verify trace continuity.

## Expected

Same trace_id appears across:

* ingestion_logs.json
* validation_logs.json
* anomaly_logs.json
* contract_logs.json
* action_logs.json

PASS / FAIL: ______

---

# Test 6 — Failure Validation

## Procedure

Run:

python test_divergence_checker.py

Mode:

duplicate

Expected:

DUPLICATE_STAGE

Mode:

sequence

Expected:

SEQUENCE_CORRUPTION

PASS / FAIL: ______

---

# Test 7 — Dashboard Validation

## Procedure

Open:

GET /dashboard

## Expected

Dashboard displays:

* Risk Level
* Anomaly Type
* Recommendation
* Trace Visibility
* Consumer Status

PASS / FAIL: ______

---

# Final Certification

Tester:

Vinayak Tiwari

Result:

☐ PASS

☐ FAIL
