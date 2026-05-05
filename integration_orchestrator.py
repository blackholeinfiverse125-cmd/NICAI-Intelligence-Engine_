from integration_adapter import run_engine
from nupur_layer import get_context_intelligence


def orchestrate_intelligence(signal: dict) -> dict:
    """
    Orchestrates:
    Validation → Sanskar → Nupur → Final Output
    """

    # Step 1: Sanskar reasoning
    sanskar_output = run_engine(signal)

    # Safety check
    if not isinstance(sanskar_output, dict) or sanskar_output.get("status") == "ERROR":
        return sanskar_output

    # Step 2: Nupur context (SAFE )
    try:
        nupur_output = get_context_intelligence(signal)
    except Exception:
        nupur_output = {
            "region_insight": "unknown",
            "spatial_risk": "unknown",
            "domain_note": "no context available"
        }

    
    # Step 3: INTELLIGENCE FUSION (REAL ORCHESTRATION)

    risk = sanskar_output.get("risk_level", "LOW")
    explanation = sanskar_output.get("explanation", "")
    recommendation = sanskar_output.get("recommendation_signal", "monitor")

    spatial_risk = nupur_output.get("spatial_risk")
    region = nupur_output.get("region_insight")
    domain = nupur_output.get("domain_note")

# 🔴 1. MODIFY RISK BASED ON CONTEXT
    if spatial_risk == "critical_zone" and risk != "HIGH":
        risk = "HIGH"
    elif spatial_risk == "polluted_zone" and risk == "LOW":
        risk = "MEDIUM"

# 🔴 2. MODIFY EXPLANATION (FUSION)
    explanation = f"{explanation} | Context: {region} classified as {spatial_risk}, {domain}."

# 🔴 3. MODIFY RECOMMENDATION
    if domain == "extreme heat zone":
        recommendation = "urgent_attention"
    elif spatial_risk == "critical_zone":
        recommendation = "eligible_for_escalation"

# 🔴 FINAL OUTPUT (NO EXTRA FIELDS)
    final_output = {
        "risk_level": risk,
        "anomaly_type": sanskar_output.get("anomaly_type"),
        "explanation": explanation,
        "temporal_context": sanskar_output.get("temporal_context"),
        "spatial_context": sanskar_output.get("spatial_context"),
        "confidence_score": sanskar_output.get("confidence_score"),
        "recommendation_signal": recommendation,
    }

    return final_output