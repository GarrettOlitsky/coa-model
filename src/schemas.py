COA_SCHEMA = {
    "type": "object",
    "required": ["accounts"],
    "properties": {
        "accounts": {
            "type": "array",
            "minItems": 8,
            "items": {
                "type": "object",
                "required": ["number", "name"],
                "properties": {
                    "number": {"type": "string"},
                    "name": {"type": "string"},
                },
                "additionalProperties": False,
            },
        }
    },
    "additionalProperties": False,
}
