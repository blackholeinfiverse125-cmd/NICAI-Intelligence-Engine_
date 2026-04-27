# NICAI — Task 5 Integration Review Packet
**Sanskar Pandey | Task 5: Full System Integration**

---

## 1. ENTRY POINT (File Paths)

| Role | File |
|------|------|
| API server | `main.py` |
| Demo runner | `run_demo_full.py` |
| Engine adapter | `integration_adapter.py` |
| Intelligence core | `sanskar_engine.py` |
| Input pipeline | `samachar_input_adapter.py` |
| Failure hardening | `error_handler.py` |
| Dashboard UI | `templates/dashboard.html` |

Start server: `uvicorn main:app --reload`
Run demo: `python run_demo_full.py`

---

## 2. CORE FLOW (3 Files)

### `main.py`
Receives `POST /nicai/evaluate` → calls `validate_signal()` → calls `run_engine()` → returns NICAI output contract.  
Also serves `/dashboard` (GET), `/action` (POST), `/run` (GET batch), `/validate` (POST), `/pipeline` (POST).

### `integration_adapter.py`
- `map_nicai_to_engine_input(signal)` → converts NICAI signal → engine dict
- `map_engine_to_nicai_output(output)` → converts engine dict → NICAI contract
- `run_engine(signal)` → full adapter pipeline, never raises

### `sanskar_engine.py`
- `SanskarEngine.process(signals)` → full analysis: preprocess → detect_anomaly → analyze_temporal → analyze_spatial → calculate_risk → calculate_confidence → generate_explanation
- `analyze_patterns(results)` → batch pattern summary

---

## 3. LIVE FLOW (Real JSON Output)

### POST /nicai/evaluate — sample input:
```json
{
  "signal_id": "S_5",
  "status": "VALID",
  "confidence_score": 0.9,
  "trace_id": "trace_auto",
  "reason": "",
  "value": { "temperature": 38.5, "aqi": 280 },
  "timestamp": "2024-06-15",
  "location": "Delhi"
}
```

### Response:
```json
{
  "signal_id": "S_5",
  "trace_id": "trace_auto",
  "risk_level": "HIGH",
  "anomaly_type": "high_pollution_with_heat",
  "explanation": "high_pollution_with_heat detected in Delhi with STABLE trend due to high pollution (AQI=280) and elevated temperature (38°C).",
  "temporal_context": "STABLE",
  "spatial_context": "Delhi",
  "confidence": 0.9,
  "recommendation_signal": "eligible_for_escalation"
}
```

### POST /action — sample:
```json
{
  "trace_id": "trace_auto",
  "action_type": "eligible_for_escalation",
  "signal_id": "S_5"
}
```
→ Written to `logs/action_logs.json`

---

## 4. WHAT WAS BUILT (Strict Bullets)

- **Phase 1**: Removed old `analyze_signal()` dead code from `sanskar_engine.py`; replaced with `SanskarEngine.process()` call via `integration_adapter.run_engine()`
- **Phase 2**: Input contract alignment — `run_engine()` accepts full NICAI signal dict; REJECT status signals return `{"status":"IGNORED"}`; all required fields mapped with safe defaults
- **Phase 3**: `integration_adapter.py` rewritten with `map_nicai_to_engine_input()` and `map_engine_to_nicai_output()` — outputs all 6 required fields: `risk_level`, `anomaly_type`, `explanation`, `temporal_context`, `confidence_score`, `recommendation_signal`
- **Phase 4**: `POST /nicai/evaluate` verified working — full pipeline: Samachar → Validation → Sanskar Engine → Output; no API route broken
- **Phase 5**: `templates/dashboard.html` redesigned — shows all 6 required fields with no blank values; confidence bar, risk colour-coding, real-time clock
- **Phase 6**: `/action` route verified — writes `action_logs.json` with correct `trace_id` and `action_type`; dashboard buttons disable after click; `signal_id` + context passed
- **Phase 7**: `run_demo_full.py` verifies all 7 steps end-to-end
- **Phase 8**: `error_handler.py` hardened — `safe_float()`, `safe_str()` helpers; all routes wrapped in try/except; engine itself returns error dict on crash instead of raising
- **Phase 9**: This review packet created at `review_packets/task5_integration.md`

---

## 5. FAILURE CASES

| Case | Handling |
|------|----------|
| Missing `signal_id` | Returns `{"status":"ERROR","reason":"Missing signal_id"}` |
| Signal status = REJECT | Returns `{"status":"IGNORED"}` |
| Missing `value` field | Returns `{"status":"ERROR","reason":"Missing value"}` |
| Missing `location` | Returns `{"status":"ERROR","reason":"Missing location"}` |
| `value` is not a dict | `map_nicai_to_engine_input` falls back to AQI=0, temp=0 |
| Engine raises exception | `run_engine` catches and returns `{"status":"ERROR","reason":"..."}` |
| CSV data not found | `load_data` prints error and returns `None, None`; route returns error |
| Empty signal list | `validate_basic_input` returns structured error |
| Log write fails | Silently skipped — server never crashes |

---

## 6. PROOF

### Before (old integration_adapter.py):
- `map_input()` only extracted `value.temperature` and `value.aqi`
- No REJECT filtering
- No `spatial_context` in output
- `confidence_score` key name mismatch (engine returns `confidence_score`, route read `confidence_score` — OK, but no normalization)

### After (new integration_adapter.py):
- Full `map_nicai_to_engine_input()` handles dict value, flat value, missing fields
- Full `map_engine_to_nicai_output()` guarantees all 6 NICAI contract fields
- REJECT signals filtered at adapter level
- Never raises — always returns dict

### /pipeline bug fixed:
- Old code: `if validation.get("status") not in ["ALLOW", "FLAG"]: return IGNORED` — but validator returns `"VALID"`, so all signals were being dropped
- New code: this check removed; VALID status passes through correctly

### Dashboard:
- Old: minimal HTML table, 4 columns, no styling, blank fields possible
- New: full NICAI-branded dashboard, 8 columns, confidence bar, action button state management, real-time clock, toast notifications
