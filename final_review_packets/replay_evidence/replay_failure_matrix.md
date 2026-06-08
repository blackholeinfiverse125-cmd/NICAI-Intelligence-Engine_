# Replay Failure Matrix

| Scenario | Failure Type | Severity | Recoverable | Recovery Action |
|-----------|-------------|-----------|-------------|----------------|
| Duplicate Stage | DUPLICATE_STAGE | MEDIUM | YES | RETRY |
| Missing Stage | MISSING_STAGE | HIGH | NO | ESCALATE |
| Sequence Corruption | SEQUENCE_CORRUPTION | HIGH | NO | ESCALATE |
| Normal Replay | NONE | NONE | N/A | PASS |

---

## Observed Results

### Duplicate Stage

Replay Status: WARNING

Recovery:
RETRY

Orchestration:
ACTIVE

---

### Missing Stage

Replay Status: FAIL

Recovery:
ESCALATE

Orchestration:
FROZEN

---

### Sequence Corruption

Replay Status: FAIL

Recovery:
ESCALATE

Orchestration:
FROZEN