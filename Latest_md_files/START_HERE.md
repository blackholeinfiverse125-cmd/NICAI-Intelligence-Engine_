# START_HERE.md

# NICAI — Start Here

## Purpose

NICAI is a bounded deterministic orchestration system for environmental intelligence processing.

The system performs:

- signal validation
- deterministic intelligence execution
- contextual fusion
- cluster aggregation
- contract governance
- replay-safe persistence
- bounded action routing

NICAI is intentionally governance-oriented and replay-safe.

The system does NOT perform autonomous real-world intervention.

---

# Primary Entry Point

Authoritative execution route:

GET /run

Located in:

main.py

This route executes the full orchestration chain.

---

# Canonical Execution Flow

Signal
→ Validation
→ Intelligence
→ Context Fusion
→ Cluster Aggregation
→ Contract Validation
→ Action Routing
→ Persistence
→ Replay Reconstruction

---

# Key Modules

| Module | Responsibility |
|---|---|
| validator.py | ingress validation |
| sanskar_engine.py | deterministic intelligence |
| integration_orchestrator.py | contextual fusion |
| cluster_intelligence.py | aggregation intelligence |
| contract_validator.py | downstream governance |
| action_router.py | bounded action routing |
| bucket_emitter.py | replay-safe persistence |
| replay_engine.py | replay reconstruction |
| main.py | canonical orchestration spine |

---

# Running NICAI

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start FastAPI server

```bash
uvicorn main:app --reload
```

---

# Main Operational Routes

| Route | Purpose |
|---|---|
| /test | health check |
| /validate | validation-only |
| /pipeline | partial orchestration |
| /nicai/evaluate | primary API integration |
| /run | canonical full orchestration |
| /dashboard | visualization layer |
| /action | action logging |

---

# Replay + Governance

Replay reconstruction:

- replay_engine.py
- lineage_exporter.py

Replay persistence:

- logs/*.json

Governance enforcement:

- contract_validator.py
- failure_handler.py

---

# Important Operational Notes

- GET /run is the authoritative governance-aware execution flow.
- Partial routes do not execute the full orchestration chain.
- Action routing is intentionally bounded and recommendation-only.
- Replay sequencing depends on immutable sequence IDs.
- Contracts are validated before action routing.

---

# Where To Start Debugging

## Replay Issues

Start with:
- replay_engine.py
- logs/*.json

## Contract Failures

Start with:
- contract_validator.py

## Intelligence Issues

Start with:
- sanskar_engine.py
- integration_orchestrator.py

## Persistence Issues

Start with:
- bucket_emitter.py

---

# Repository State

NICAI has been operationally audited for:

- replay governance
- contract enforcement
- deterministic orchestration
- lineage persistence
- contextual fusion
- bounded execution

System status:

OPERATIONALLY_RESILIENT