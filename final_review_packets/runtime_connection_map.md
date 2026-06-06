# Runtime Connection Map

## Objective

Validate runtime participant wiring and execution flow across the NICAI operational convergence chain.

---

## Participant Flow

SAMACHAR / GUPTACHAR
↓
NICAI ORCHESTRATION
↓
CONTRACT VALIDATION
↓
ACTION ROUTER
↓
TANTRA
↓
TTG
↓
REPLAY ENGINE
↓
DASHBOARD

---

## Runtime Connections

| Upstream | Downstream | Contract |
|-----------|------------|----------|
| Samachar Input Adapter | NICAI | Signal Contract |
| NICAI | Contract Validator | Analysis Contract |
| Contract Validator | Action Router | Validated Contract |
| Action Router | TANTRA | Consumer Contract |
| TANTRA | TTG | Participation Event |
| TTG | Replay Engine | Execution Event |
| Replay Engine | Dashboard | Replay Summary |

---

## Trace Propagation

Single Trace Example:

trace_06d37c78

Observed Through:

INGESTION
VALIDATION
ANALYSIS
CLUSTER_ANALYSIS
CONTRACT_VALIDATION
ACTION
TANTRA_PARTICIPATION
TTG_CONSUME

---

## Result

All runtime participants successfully connected and operational.