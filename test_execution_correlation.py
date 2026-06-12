from execution_correlation import (
    build_execution_correlation,
    export_execution_correlation
)

print("\nEXECUTION CORRELATION TEST\n")

result = build_execution_correlation(

    execution_id="exec-tantra-001",

    trace_id="trace_ccea9ad2",

    contract_id="NICAI_ENVIRONMENTAL_V1",

    consumer_name="TANTRA"
)

print(result)

export_execution_correlation(
    result
)

print("\nEXPORTED\n")