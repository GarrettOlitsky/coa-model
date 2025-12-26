from __future__ import annotations
import argparse
from .prompts import SYSTEM_PROMPT, USER_TEMPLATE
from .model_client import ModelClient
from .validators import validate_schema, normalize_accounts, sanity_check_numbering
from .excel_writer import write_coa_xlsx
from .schemas import COA_SCHEMA

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a Chart of Accounts (Excel) from an entity description.")
    p.add_argument("--type", required=True, choices=["for-profit", "nonprofit"], help="Entity type")
    p.add_argument("--name", required=True, help="Entity name")
    p.add_argument("--desc", required=True, help="Entity description (quoted string)")
    p.add_argument("--out", default="Chart_of_Accounts.xlsx", help="Output XLSX path")
    return p.parse_args()

def run(entity_type: str, entity_name: str, description: str, out_path: str,
        hints: list[str] | None = None,
        top_vendors: list[dict] | None = None,
        raw_excerpt: str = "") -> None:

    hints = hints or []
    top_vendors = top_vendors or []

    user_prompt = USER_TEMPLATE.format(
        entity_type=entity_type,
        entity_name=entity_name,
        description=description,
        hints=hints,
        top_vendors=top_vendors,
        raw_excerpt=raw_excerpt,
    )

    client = ModelClient()
    payload = client.call_model(SYSTEM_PROMPT, user_prompt, json_schema=COA_SCHEMA)

    validate_schema(payload)
    accounts = normalize_accounts(payload)
    sanity_check_numbering(accounts)

    write_coa_xlsx(accounts, out_path)

def main() -> None:
    args = parse_args()
    run(args.type, args.name, args.desc, args.out)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
