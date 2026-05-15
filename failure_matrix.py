FAILURE_MATRIX = {

    "MISSING_STAGE": {
        "severity": "HIGH",
        "recoverable": False,
        "category": "REPLAY_FAILURE"
    },

    "SEQUENCE_CORRUPTION": {
        "severity": "HIGH",
        "recoverable": False,
        "category": "LINEAGE_FAILURE"
    },

    "DUPLICATE_STAGE": {
        "severity": "MEDIUM",
        "recoverable": True,
        "category": "REPLAY_FAILURE"
    },

    "INVALID_CONTRACT": {
        "severity": "HIGH",
        "recoverable": False,
        "category": "CONTRACT_FAILURE"
    },

    "TRACE_MISMATCH": {
        "severity": "HIGH",
        "recoverable": False,
        "category": "TRACE_FAILURE"
    },

    "UNKNOWN_FAILURE": {
        "severity": "LOW",
        "recoverable": True,
        "category": "GENERIC_FAILURE"
    }
}