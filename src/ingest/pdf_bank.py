from __future__ import annotations
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

import pdfplumber

VENDOR_RE = re.compile(r"[A-Z0-9][A-Z0-9 &\-\./]{2,}")

@dataclass
class EvidencePack:
    raw_text_excerpt: str
    top_vendors: list[dict]
    hints: list[str]

def extract_text_from_pdf(pdf_path: str, max_pages: int = 3) -> str:
    chunks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            text = page.extract_text() or ""
            if text.strip():
                chunks.append(text)
    return "\n\n".join(chunks).strip()

def build_evidence_pack_from_pdf_text(text: str, top_n: int = 12) -> EvidencePack:
    # crude but useful MVP: vendor-ish tokens from ALLCAPS-ish lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    vendor_hits = []

    hints = []
    joined = "\n".join(lines).upper()
    for kw, hint in [
        ("SQUARE", "POS/processor likely (Square)"),
        ("STRIPE", "POS/processor likely (Stripe)"),
        ("PAYROLL", "Payroll activity detected"),
        ("GUSTO", "Payroll provider likely (Gusto)"),
        ("ADP", "Payroll provider likely (ADP)"),
        ("LOAN", "Loan-related activity detected"),
        ("INTEREST", "Interest expense likely"),
        ("ATM", "Cash withdrawals likely"),
        ("WIRE", "Wire activity likely"),
        ("ZELLE", "Zelle transfers likely"),
    ]:
        if kw in joined:
            hints.append(hint)

    for ln in lines:
        m = VENDOR_RE.search(ln.upper())
        if m:
            token = m.group(0).strip()
            # avoid obvious junk headers
            if token not in {"STATEMENT", "BALANCE", "ACCOUNT", "DATE", "DESCRIPTION"} and len(token) <= 40:
                vendor_hits.append(token)

    counts = Counter(vendor_hits)
    top = [{"vendor": v, "count": c} for v, c in counts.most_common(top_n)]

    excerpt = text[:4000]  # keep prompt small
    return EvidencePack(raw_text_excerpt=excerpt, top_vendors=top, hints=hints)
