from __future__ import annotations
import json
import os
from typing import Any

class ModelClient:
    """
    Uses OpenAI if OPENAI_API_KEY is set. Otherwise falls back to stub.
    OpenAI Structured Outputs / JSON mode supported via response_format. :contentReference[oaicite:0]{index=0}
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()

    def call_model(self, system: str, user: str, json_schema: dict | None = None) -> dict:
        if not self.api_key:
            return self._stub_response()

        try:
            from openai import OpenAI
        except Exception:
            # If openai library isn't installed for some reason, fallback
            return self._stub_response()

        client = OpenAI(api_key=self.api_key)

        # Prefer Structured Outputs (json_schema) when provided. :contentReference[oaicite:1]{index=1}
        response_format: dict[str, Any]
        if json_schema:
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "chart_of_accounts",
                    "strict": True,
                    "schema": json_schema,
                },
            }
        else:
            response_format = {"type": "json_object"}  # older JSON mode :contentReference[oaicite:2]{index=2}

        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format=response_format,
        )

        content = resp.choices[0].message.content or "{}"
        return json.loads(content)

    def _stub_response(self) -> dict:
        return {
            "accounts": [
                {"number": "1010", "name": "Operating Checking"},
                {"number": "1100", "name": "Accounts Receivable"},
                {"number": "1200", "name": "Inventory"},
                {"number": "1500", "name": "Furniture & Equipment"},
                {"number": "2000", "name": "Accounts Payable"},
                {"number": "2100", "name": "Credit Card Payable"},
                {"number": "3000", "name": "Owner's Equity"},
                {"number": "4000", "name": "Sales Revenue"},
                {"number": "6100", "name": "Rent Expense"},
                {"number": "6260", "name": "Merchant Processing Fees"},
                {"number": "6400", "name": "Payroll Expense"},
                {"number": "6500", "name": "Repairs & Maintenance"},
            ]
        }
