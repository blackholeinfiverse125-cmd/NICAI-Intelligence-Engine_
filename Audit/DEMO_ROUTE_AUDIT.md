# DEMO_ROUTE_AUDIT.md

## Objective

Audit all exposed NICAI routes and determine the authoritative execution path for the Task 11 Demo Convergence Sprint.

---

# Route 1 — /test

### Method

GET

### Purpose

Health check endpoint used to verify API availability.

### Execution Flow

System Check
→ Return Status

### Executes

* API availability verification

### Does Not Execute

* Validation
* Intelligence
* Context Fusion
* Cluster Analysis
* Contract Validation
* Action Routing
* Persistence
* Replay Validation
* Dashboard Rendering

### Assessment

Role: Infrastructure Health Check

Canonical Demo Route: NO

---

# Route 2 — /validate

### Method

POST

### Purpose

Validate a single incoming signal against NICAI validation rules.

### Execution Flow

Input Signal
→ validate_signal()
→ Return Validation Result

### Executes

* Signal validation
* Error handling
* IGNORED signal handling

### Does Not Execute

* Intelligence
* Context Fusion
* Cluster Analysis
* Contract Validation
* Action Routing
* Persistence
* Replay Validation
* Dashboard Rendering

### Assessment

Role: Validation Testing Endpoint

Canonical Demo Route: NO

---

# Route 3 — /pipeline

### Method

POST

### Purpose

Execute validation and intelligence processing for a single signal.

### Execution Flow

Input Signal
→ Validation
→ orchestrate_intelligence()
→ Return Intelligence Output

### Executes

* Validation
* Intelligence processing
* Context layer invocation through orchestrator

### Does Not Execute

* Cluster Analysis
* Contract Validation
* Action Routing
* Persistence
* Replay Validation
* Dashboard Rendering
* TANTRA Participation
* TTG Consumption

### Assessment

Role: Single Signal Intelligence Endpoint

Canonical Demo Route: NO

---

# Route 4 — /nicai/evaluate

### Method

POST

### Purpose

Official NICAI signal evaluation endpoint.

### Execution Flow

Input Signal
→ Validation
→ orchestrate_intelligence()
→ Build Output Contract
→ Persist Analysis Output
→ Return Response

### Executes

* Validation
* Intelligence processing
* Output contract generation
* Analysis persistence

### Persistence

Writes:

anomaly_logs.json

### Does Not Execute

* Cluster Analysis
* Contract Validation
* Action Routing
* Replay Validation
* Dashboard Rendering
* TANTRA Participation
* TTG Consumption

### Assessment

Role: Official Signal Evaluation Endpoint

Canonical Demo Route: NO

---

# Route 5 — /run

### Method

GET

### Purpose

Execute the complete NICAI operational chain using dataset inputs.

### Execution Flow

Dataset Load
→ Signal Conversion
→ Validation
→ Intelligence
→ Context Fusion
→ Analysis Persistence
→ Cluster Analysis
→ Contract Validation
→ Action Routing
→ TANTRA Participation
→ TTG Consumption
→ Return Execution Results

### Executes

* Dataset Loading
* Validation
* Intelligence Processing
* Context Layer Invocation
* Analysis Persistence
* Cluster Analysis
* Contract Validation
* Action Routing
* TANTRA Participation
* TTG Consumption

### Persistence

Writes:

* ingestion_logs.json
* validation_logs.json
* anomaly_logs.json
* pattern_logs.json
* contract_logs.json

### Missing

* Automatic Replay Validation
* Automatic Dashboard Launch

### Assessment

Role: Full Operational Execution Route

Canonical Demo Route: YES

---

# Route 6 — /dashboard

### Method

GET

### Purpose

Operational visualization layer.

### Execution Flow

Dataset Load
→ Validation
→ Intelligence
→ Dashboard Rendering

### Executes

* Dashboard Rendering
* Consumer Registry Visibility
* Execution Correlation Visibility
* Consumer Health Visibility
* Replay Status Visibility

### Does Not Execute

* Cluster Analysis
* Contract Validation
* Action Routing
* TANTRA Participation
* TTG Consumption
* Replay Validation

### Assessment

Role: Operational Visibility Surface

Canonical Demo Route: NO

Operational Surface: YES

---

# Route 7 — /action

### Method

POST

### Purpose

Accept manual operator actions from dashboard.

### Execution Flow

Dashboard Action
→ Build Action Payload
→ Persist Action
→ Return Success

### Executes

* Action Logging
* Trace Mapping
* Operator Interaction Persistence

### Persistence

Writes:

action_logs.json

### Does Not Execute

* Validation
* Intelligence
* Context Fusion
* Cluster Analysis
* Contract Validation
* Replay Validation
* Dashboard Rendering
* TANTRA Participation
* TTG Consumption

### Assessment

Role: Manual Operator Action Endpoint

Canonical Demo Route: NO

 #Route Capability Matrix

| Route             | Validation | Intelligence | Cluster | Contract | Action | Persistence | Dashboard |
| ----------------- | ---------- | ------------ | ------- | -------- | ------ | ----------- | --------- |
| `/test`           | ❌          | ❌            | ❌       | ❌        | ❌      | ❌           | ❌         |
| `/validate`       | ✅          | ❌            | ❌       | ❌        | ❌      | ❌           | ❌         |
| `/pipeline`       | ✅          | ✅            | ❌       | ❌        | ❌      | ❌           | ❌         |
| `/nicai/evaluate` | ✅          | ✅            | ❌       | ❌        | ❌      | ✅           | ❌         |
| `/run`            | ✅          | ✅            | ✅       | ✅        | ✅      | ✅           | ❌         |
| `/dashboard`      | ✅          | ✅            | ❌       | ❌        | ❌      | ❌           | ✅         |
| `/action`         | ❌          | ❌            | ❌       | ❌        | ✅      | ✅           | ❌         |


---

# Final Route Classification

| Route           | Role                         | Canonical |
| --------------- | ---------------------------- | --------- |
| /test           | Health Check                 | NO        |
| /validate       | Validation Endpoint          | NO        |
| /pipeline       | Single Signal Intelligence   | NO        |
| /nicai/evaluate | Official Evaluation Endpoint | NO        |
| /run            | Full Operational Chain       | YES       |
| /dashboard      | Visualization Surface        | NO        |
| /action         | Manual Action Endpoint       | NO        |

---

# Canonical Demo Path

GET /run

Execution Chain:

Dataset
→ Validation
→ Intelligence
→ Context Fusion
→ Cluster Analysis
→ Contract Validation
→ Action Routing
→ Persistence
→ TANTRA Participation
→ TTG Consumption

Operational Visibility:

GET /dashboard

---

# Phase 1 Conclusion

The authoritative execution route for the NICAI Task 11 Demo Convergence Sprint is:

GET /run

All other routes are supporting, testing, visualization, or operator interaction routes.