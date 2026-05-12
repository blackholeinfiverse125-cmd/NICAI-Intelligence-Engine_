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
            "confidence": 0.0,
            "recommendation_signal": "monitor",
        }

    total = len(processed)

    # Extract actual data
    data_list = processed
    composite_heat_pollution = 0

    for item in data_list:

        explanation_text = item.get("explanation", "").lower()

        if (
            "pollution" in explanation_text
            and "heat" in explanation_text
        ):
            composite_heat_pollution += 1

    composite_detected = composite_heat_pollution >= 2
    high_count = sum(1 for d in data_list if d.get("risk_level") == "HIGH")
    medium_count = sum(1 for d in data_list if d.get("risk_level") == "MEDIUM")
    # ---------------------------------
# TEMPORAL ESCALATION DETECTION
# ---------------------------------

    consecutive_high = 0
    max_consecutive_high = 0

    for item in data_list:

        if item.get("risk_level") == "HIGH":
            consecutive_high += 1

        if consecutive_high > max_consecutive_high:
            max_consecutive_high = consecutive_high

        else:
            consecutive_high = 0

    temporal_wave_detected = max_consecutive_high >= 3
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
        item.get("spatial_context")
        for item in processed
        if item.get("spatial_context")
    ]
    unique_regions = list(set(regions))
    multi_region_cluster = len(unique_regions) >= 3
    
    region = regions[0] if regions else "unknown"

    explanation = (
        f"Cluster analysis: {high_count}/{total} HIGH risk signals, "
        f"{medium_count}/{total} MEDIUM. "
        f"Situation classified as {risk}. "
        f"Context: Elevated environmental risk observed in {region}."
    )

    if temporal_wave_detected:
        explanation += (
            " Sustained temporal escalation detected "
            "through consecutive HIGH-risk signals."
        )
    if multi_region_cluster:
        explanation += (
            f" Multi-region spread detected across "
            f"{len(unique_regions)} regions."
        )
    if composite_detected:
        explanation += (
            " Composite environmental stress detected "
            "from interacting pollution and heat indicators."
        )   
    # RULE 4 — recommendation
    '''if risk == "HIGH":
        recommendation = "eligible_for_escalation"
    elif risk == "MEDIUM":
        recommendation = "requires_review"
    else:
        recommendation = "monitor"   '''
    
    escalation_score = 0

    if risk == "HIGH":
        escalation_score += 3

    elif risk == "MEDIUM":
        escalation_score += 2

    else:
        escalation_score += 1

    if temporal_wave_detected:
        escalation_score += 2

    if multi_region_cluster:
        escalation_score += 2

    if composite_detected:
        escalation_score += 3

# ---------------------------------
# ESCALATION ROUTING
# ---------------------------------

    if escalation_score >= 7:
        recommendation = "eligible_for_escalation"
    elif escalation_score >= 4:
        recommendation = "requires_review"

    else:
        recommendation = "monitor"

    # 🔥 TRACE CONTINUITY (CRITICAL)
    trace_id = next(
        (item.get("trace_id") for item in processed if item.get("trace_id")),
        "unknown"
    )
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