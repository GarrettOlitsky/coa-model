from __future__ import annotations
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .schemas import COA_SCHEMA

def validate_schema(payload: dict) -> None:
    try:
        validate(instance=payload, schema=COA_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Model output failed schema validation: {e.message}") from e

def normalize_accounts(payload: dict) -> list[dict]:
    accounts = payload["accounts"]

    clean: list[dict] = []
    seen = set()

    for a in accounts:
        num = str(a["number"]).strip()
        name = str(a["name"]).strip()
        if not num or not name:
            continue

        key = (num, name.lower())
        if key in seen:
            continue
        seen.add(key)

        clean.append({"number": num, "name": name})

    if len(clean) < 8:
        raise ValueError("Too few accounts after normalization; model output is not usable.")

    return clean

def sanity_check_numbering(accounts: list[dict]) -> None:
    def bucket(n: int) -> str:
        if 1000 <= n <= 1999: return "assets"
        if 2000 <= n <= 2999: return "liabilities"
        if 3000 <= n <= 3999: return "equity_or_net_assets"
        if 4000 <= n <= 4999: return "revenue"
        if 5000 <= n <= 5999: return "cogs"
        if 6000 <= n <= 6999: return "opex"
        if 7000 <= n <= 7999: return "other_income"
        if 8000 <= n <= 8999: return "other_expense"
        return "out_of_range"

    bad = []
    for a in accounts:
        try:
            n = int(a["number"])
        except ValueError:
            bad.append(a)
            continue
        if bucket(n) == "out_of_range":
            bad.append(a)

    if bad:
        sample = "; ".join([f'{x["number"]} {x["name"]}' for x in bad[:5]])
        raise ValueError(f"Some account numbers are out of expected ranges. Examples: {sample}")
