from consumer_registry import (
    load_registry,
    lookup_consumer,
    validate_consumer,
    get_allowed_contracts
)

print("\nREGISTRY LOAD TEST\n")

registry = load_registry()

print(
    f"Consumers Loaded: "
    f"{len(registry.get('consumers', []))}"
)

print("\nLOOKUP TEST\n")

print(
    lookup_consumer("TANTRA")
)

print(
    lookup_consumer("TTG")
)

print("\nVALIDATION TEST\n")

print(
    validate_consumer("TANTRA")
)

print(
    validate_consumer("TTG")
)

print(
    validate_consumer("FAKE_CONSUMER")
)

print("\nCONTRACT TEST\n")

print(
    get_allowed_contracts("TANTRA")
)

print(
    get_allowed_contracts("TTG")
)