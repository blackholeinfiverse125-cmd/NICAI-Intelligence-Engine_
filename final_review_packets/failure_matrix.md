# Failure Matrix

## Objective

Validate runtime failure detection and recovery.

---

| Failure Type | Detection | Recovery |
|-------------|------------|-----------|
| Missing Contract | PASS | Detected |
| Invalid Consumer | PASS | Detected |
| Trace Break | PASS | Detected |
| Duplicate Event | PASS | RETRY |
| Missing Replay Stage | PASS | Detected |

---

## Runtime Evidence

Duplicate Event Test

Trace:
trace_06d37c78

Result:

divergence_detected = true

failure_type = DUPLICATE_STAGE

severity = MEDIUM

recoverable = true

---

## Recovery Action

RETRY

orchestration_status = ACTIVE

---

## Governance Telemetry

total_failures = 1

recoverable_failures = 1

non_recoverable_failures = 0

---

## Conclusion

Failure detection and recovery mechanisms operational.