from contract_validator import validate_contract

bad_output = {
    "trace_id": "trace_test",
    "risk_level": "EXTREME",
    "recommendation_signal": "random_action",
    "confidence": 9
}

result = validate_contract(bad_output)

print(result)