def analyze_signal_cluster(processed: list) -> dict:
    """
    Phase 2 + Phase 4 — Multi-signal intelligence with trace continuity
    """

    if not processed:
        return {
            "trace_id": "unknown",
            "risk_level": "LOW",
            "anomaly_type": "no_data",
            "explanation": "No signals available.",
            "temporal_context": "UNKNOWN",
            "spatial_context": "UNKNOWN",
            "confidence_score": 0.0,
            "recommendation_signal": "monitor",
        }

    total = len(processed)

    # Extract actual data
    data_list = [item.get("data", {}) for item in processed]

    high_count = sum(1 for d in data_list if d.get("risk_level") == "HIGH")
    medium_count = sum(1 for d in data_list if d.get("risk_level") == "MEDIUM")

    # RULE 1 — risk escalation
    if high_count >= total * 0.5:
        risk = "HIGH"
    elif (high_count + medium_count) >= total * 0.5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # RULE 2 — anomaly type
    if risk == "HIGH":
        anomaly = "clustered_severe_environmental_risk"
    elif risk == "MEDIUM":
        anomaly = "clustered_moderate_environmental_risk"
    else:
        anomaly = "normal_conditions"

    # RULE 3 — explanation
    #region = processed[0].get("spatial_context", "unknown")
    regions = [
        item.get("data", {}).get("spatial_context")
        for item in processed
        if item.get("data", {}).get("spatial_context")  
    ]
    region = regions[0] if regions else "unknown"

    explanation = (
        f"Cluster analysis: {high_count}/{total} HIGH risk signals, "
        f"{medium_count}/{total} MEDIUM. Situation classified as {risk}. "
        f"Context: Elevated environmental risk observed in {region}."
    )

    # RULE 4 — recommendation
    if risk == "HIGH":
        recommendation = "eligible_for_escalation"
    elif risk == "MEDIUM":
        recommendation = "requires_review"
    else:
        recommendation = "monitor"

    # 🔥 TRACE CONTINUITY (CRITICAL)
    trace_id = processed[0].get("trace_id", "unknown")
    spatial_context = region
    return {
        "trace_id": trace_id,
        "risk_level": risk,
        "anomaly_type": anomaly,
        "explanation": explanation,
        "temporal_context": "CLUSTERED",
        "spatial_context": spatial_context,
        "confidence": 0.9,
        "recommendation_signal": recommendation,
    }