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

    # Step 3: Merge outputs
    final_output = {**sanskar_output, **nupur_output}

    return final_output