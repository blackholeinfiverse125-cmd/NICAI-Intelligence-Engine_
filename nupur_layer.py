def get_context_intelligence(signal: dict) -> dict:
    """
    Nupur Layer — Context + Spatial Intelligence
    """
    
    location = signal.get("location", "unknown")
    value = signal.get("value", {})

    pollution = value.get("aqi", 0)
    temperature = value.get("temperature", 0)

    # Spatial / regional reasoning
    if pollution >= 300:
        spatial_risk = "critical_zone"
    elif pollution >= 150:
        spatial_risk = "polluted_zone"
    else:
        spatial_risk = "normal_zone"

    # Domain insight
    if temperature >= 40:
        domain_note = "extreme heat zone"
    elif temperature >= 35:
        domain_note = "heat stress zone"
    else:
        domain_note = "stable climate"

    return {
        "region_insight": location,
        "spatial_risk": spatial_risk,
        "domain_note": domain_note
    }