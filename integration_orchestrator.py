from integration_adapter import run_engine
from nupur_layer import get_context_intelligence


def orchestrate_intelligence(signal: dict) -> dict:
    """
    Orchestrates:
    Validation → Sanskar → Nupur → Final Output
    """

    # Step 1: Sanskar reasoning
    sanskar_output = run_engine(signal)

    if not isinstance(sanskar_output, dict) or sanskar_output.get("status") == "ERROR":
        return sanskar_output

    # Step 2: Nupur context
    try:
        nupur_output = get_context_intelligence(signal)
    except Exception:
        nupur_output = {
            "region_insight": "unknown",
            "spatial_risk": "unknown",
            "domain_note": "no context available"
        }

    # -------------------------------
    #  PHASE 1 — REAL FUSION
    # -------------------------------

    risk = sanskar_output.get("risk_level", "LOW")
    explanation = sanskar_output.get("explanation", "")
    recommendation = sanskar_output.get("recommendation_signal", "monitor")

    spatial_risk = nupur_output.get("spatial_risk")
    region = nupur_output.get("region_insight")
    domain = nupur_output.get("domain_note")

    # 1️MODIFY RISK (STRONG FUSION)
    if spatial_risk == "critical_zone" and risk != "HIGH":
        risk = "HIGH"
    elif spatial_risk == "polluted_zone" and risk == "LOW":
        risk = "MEDIUM"

    # 2️ MODIFY EXPLANATION
    explanation = (
        f"{explanation} | Context: {region} classified as {spatial_risk}, {domain}."
    )

    # 3️ MODIFY RECOMMENDATION (DECISION-LEVEL CHANGE)
    if domain == "extreme heat zone":
        recommendation = "eligible_for_escalation"
    elif spatial_risk == "critical_zone":
        recommendation = "eligible_for_escalation"

    # -------------------------------
    # PHASE 4 — TRACE CONTINUITY
    # -------------------------------
    trace_id = sanskar_output.get("trace_id", signal.get("trace_id", "unknown"))

    # -------------------------------
    #  PHASE 5 — CONTRACT LOCK
    # -------------------------------
    final_output = {
        "trace_id": trace_id,  #  REQUIRED
        "risk_level": risk,
        "anomaly_type": sanskar_output.get("anomaly_type"),
        "explanation": explanation,
        "temporal_context": sanskar_output.get("temporal_context"),
        "spatial_context": sanskar_output.get("spatial_context"),
        "confidence": sanskar_output.get("confidence", 0.5),
        "recommendation_signal": recommendation,
    }

    return final_output