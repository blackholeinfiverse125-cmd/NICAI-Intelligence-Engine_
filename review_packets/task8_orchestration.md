# NICAI Task 8 — Intelligence Orchestration Layer

## 1. ENTRY POINT

The orchestration flow begins at the FastAPI endpoint:

POST /nicai/evaluate

This endpoint:

* Receives validated signal input
* Passes signal to orchestration layer
* Returns unified intelligence output

---

## 2. CORE FLOW (Max 3 files)

The system operates through three core components:

1. main.py
   → Handles API request and validation flow

2. integration_orchestrator.py
   → Controls orchestration logic
   → Calls Sanskar + Nupur layers

3. nupur_layer.py
   → Adds contextual and spatial intelligence

---

## 3. LIVE FLOW (Execution Pipeline)

Signal Input → Validation → Orchestrator → Final Output

Step-by-step:

1. Input signal received via API
2. Validation layer checks signal integrity
3. Orchestrator calls:

   * Sanskar engine → anomaly detection + risk scoring
   * Nupur layer → contextual intelligence
4. Outputs are merged
5. Final unified response returned

---

## 4. HOW SANSKAR + NUPUR ARE MERGED

Sanskar Layer:

* Provides:
  risk_level
  anomaly_type
  explanation
  temporal_context
  spatial_context
  confidence_score
  recommendation_signal

Nupur Layer:

* Provides:
  region_insight
  spatial_risk
  domain_note

Final Output:

* Combined into a single dictionary
* Context enriches explanation without duplicating logic
* No independent decisions are made by Nupur layer

---

## 5. FAILURE CASES

Handled scenarios:

1. Invalid input
   → Returns error response

2. Validation failure
   → Signal ignored or rejected

3. Nupur layer failure
   → System continues with Sanskar output

4. Missing context data
   → Default fallback values used

System never crashes and always returns valid output.

---

## 6. TRACEABILITY PROOF

Trace ID is preserved across all layers:

Validation → Orchestrator → Output → Logs

Each response contains:

* trace_id
* timestamp
* full intelligence output

Logs are stored in structured JSON format for tracking.

---

## 7. FINAL SYSTEM STATE

The system is now:

* Deterministic
* Layered
* Modular
* API-driven
* Context-aware

It produces a unified intelligence output combining:

* anomaly reasoning
* risk scoring
* spatial context
* domain insights

No duplication, no contradictions, and no logic overlap exist.

---

## 8. SAMPLE OUTPUT (Combined Intelligence)

Example:

{
"risk_level": "HIGH",
"anomaly_type": "severe_environmental_risk",
"explanation": "Air quality in Delhi is extremely poor (AQI 320) combined with high temperature (40°C), indicating severe environmental risk.",
"temporal_context": "STABLE",
"spatial_context": "Delhi",
"confidence_score": 0.95,
"recommendation_signal": "eligible_for_escalation",
"region_insight": "Delhi",
"spatial_risk": "critical_zone",
"domain_note": "extreme heat zone"
}
