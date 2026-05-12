# Failure Matrix

| Failure Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|
| Empty payload | Structured rejection | Structured ERROR returned | PASSED |
| Missing fields | Validation failure | Validation rejection visible | PASSED |
| Invalid contract | Downstream rejection | Contract blocked | PASSED |
| Replay invalid trace | No replay entries | Graceful replay failure | PASSED |
| Contract corruption | Failure containment | Deterministic error returned | PASSED |
| Invalid schema types | Validation rejection | Structured rejection | PASSED |
| Large signal batch | Stable execution | No crash observed | PASSED |

---

# Conclusion

NICAI failure handling is deterministic, observable, replay-safe, and contract-enforced.