from contract_validator import validate_contract

print("\nVALID CONTRACT\n")

valid_contract = {
    "trace_id": "trace_demo",
    "risk_level": "HIGH",
    "anomaly_type": "pollution",
    "explanation": "High pollution detected",
    "temporal_context": "RISING",
    "spatial_context": "Mumbai",
    "confidence": 0.9,
    "recommendation_signal": "requires_review"
}

print(validate_contract(valid_contract))


print("\nMISSING FIELD TEST\n")

missing_field = {
    "trace_id": "trace_demo"
}

print(validate_contract(missing_field))


print("\nINVALID RISK LEVEL TEST\n")

invalid_risk = dict(valid_contract)
invalid_risk["risk_level"] = "CRITICAL"

print(validate_contract(invalid_risk))


print("\nINVALID CONFIDENCE TEST\n")

invalid_confidence = dict(valid_contract)
invalid_confidence["confidence"] = 5

print(validate_contract(invalid_confidence))


print("\nINVALID RECOMMENDATION TEST\n")

invalid_recommendation = dict(valid_contract)
invalid_recommendation["recommendation_signal"] = "DO_SOMETHING"

print(validate_contract(invalid_recommendation))