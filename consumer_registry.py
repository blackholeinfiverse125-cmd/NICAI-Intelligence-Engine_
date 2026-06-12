import json


REGISTRY_FILE = "contracts/consumer_registry.json"


def load_registry():
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Registry load error: {e}")
        return {"consumers": []}


def lookup_consumer(consumer_name):
    registry = load_registry()

    for consumer in registry.get("consumers", []):
        if consumer.get("consumer_name") == consumer_name:
            return consumer

    return None


def validate_consumer(consumer_name):
    consumer = lookup_consumer(consumer_name)

    if consumer is None:
        return {
            "consumer_valid": False,
            "reason": "UNKNOWN_CONSUMER"
        }

    if consumer.get("status") != "ACTIVE":
        return {
            "consumer_valid": False,
            "reason": "INACTIVE_CONSUMER"
        }

    return {
        "consumer_valid": True,
        "consumer": consumer
    }


def get_allowed_contracts(consumer_name):
    consumer = lookup_consumer(consumer_name)

    if consumer is None:
        return []

    return consumer.get("allowed_contracts", [])