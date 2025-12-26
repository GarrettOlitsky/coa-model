SYSTEM_PROMPT = """You are an expert accountant.
Generate a practical Chart of Accounts tailored to the entity.
Return ONLY valid JSON. No markdown. No commentary."""

USER_TEMPLATE = """
Entity name: {entity_name}
Entity type: {entity_type}  (for-profit or nonprofit)

Entity description:
{description}

Optional evidence from uploaded docs (may be empty):
- Hints: {hints}
- Top vendors/merchants: {top_vendors}
- Raw excerpt (truncated): {raw_excerpt}

Rules:
- Use a coherent numbering scheme:
  Assets 1000-1999, Liabilities 2000-2999, Equity/Net Assets 3000-3999,
  Revenue 4000-4999, COGS 5000-5999 (if applicable), Operating Expenses 6000-6999,
  Other Income/Gains 7000-7999, Other Expenses/Losses 8000-8999.
- Prefer accounts supported by evidence (e.g., merchant fees if Square/Stripe shows up; loan payable/interest if loan hints appear; payroll accounts if payroll hints appear).
- Avoid duplicates and overly granular noise.

Output JSON with schema:
{{
  "accounts": [
    {{ "number": "1010", "name": "Operating Checking" }}
  ]
}}
"""
