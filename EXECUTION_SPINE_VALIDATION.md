# NICAI — Single Execution Spine Validation

## Objective

Validate that NICAI executes as one bounded deterministic orchestration system.

This document identifies:

- canonical execution spine
- orchestration ordering
- governance checkpoints
- replay continuity
- contract enforcement boundaries
- duplicate execution paths
- partial execution routes
- operational limitations

No assumptions are included.

Validation based only on actual repository implementation.

---

# Canonical Execution Spine

Authoritative execution route:

GET /run

Located in:

main.py

This is the only route executing the complete bounded governance chain.

---

# Full Execution Flow

Signal
→ validate_signal()
→ orchestrate_intelligence()
→ analyze_signal_cluster()
→ validate_contract()
→ route_action()
→ emit_bucket_artifact()
→ emit_orchestration_event()
→ replay/governance visibility

---

# Execution Layer Breakdown

## 1. Validation Layer

Module:
- validator.py
- main.py validate_signal()

Responsibilities:
- signal validation
- trace assignment
- schema checks
- ingress governance
- failure normalization

Replay-safe:
YES

---

## 2. Intelligence Layer

Module:
- sanskar_engine.py

Responsibilities:
- anomaly detection
- temporal reasoning
- spatial reasoning
- deterministic escalation
- explanation generation

Replay-safe:
YES

---

## 3. Context Fusion Layer

Module:
- integration_orchestrator.py

Responsibilities:
- Nupur contextual fusion
- contextual escalation
- explanation enrichment
- trace continuity preservation

Replay-safe:
YES

---

## 4. Aggregation Layer

Module:
- cluster_intelligence.py

Responsibilities:
- multi-signal aggregation
- temporal wave analysis
- regional spread analysis
- escalation scoring

Replay-safe:
YES

---

## 5. Contract Governance Layer

Module:
- contract_validator.py

Responsibilities:
- required field validation
- enum enforcement
- confidence bounds validation
- downstream contract gating

Replay-safe:
YES

---

## 6. Action Governance Layer

Module:
- action_router.py

Responsibilities:
- bounded action routing
- escalation emission
- operational decision mapping

Replay-safe:
YES

---

## 7. Persistence + Replay Layer

Modules:
- bucket_emitter.py
- replay_engine.py

Responsibilities:
- immutable sequencing
- lineage persistence
- replay reconstruction
- stage continuity verification

Replay-safe:
YES

---

# Governance Boundaries

NICAI enforces bounded execution through:

- validation-first orchestration
- deterministic escalation
- contract validation before action routing
- replay-safe persistence
- immutable sequencing
- bounded recommendation-only actions

NICAI does NOT autonomously execute real-world interventions.

---

# Partial Execution Routes

The following routes execute only partial orchestration:

| Route | Limitation |
|---|---|
| /validate | validation only |
| /pipeline | no aggregation/governance chain |
| /nicai/evaluate | partial orchestration |
| /dashboard | visualization-only execution |

These are not canonical execution paths.

---

# Canonical Spine Conclusion

The authoritative operational execution spine of NICAI is:

GET /run

This route is the only fully integrated governance-aware deterministic execution flow currently implemented.