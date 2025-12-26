import os
import tempfile
import streamlit as st

from src.main import run
from src.ingest.pdf_bank import extract_text_from_pdf, build_evidence_pack_from_pdf_text

st.set_page_config(page_title="Chart of Accounts Model", layout="centered")

st.title("Chart of Accounts Model")
st.caption("Describe an entity + optionally upload a bank statement PDF. Generates a 2-column Excel Chart of Accounts.")

entity_type = st.selectbox("Entity type", ["for-profit", "nonprofit"])
entity_name = st.text_input("Entity name", value="REGAL ALE")
description = st.text_area(
    "Describe the entity (industry, revenue streams, costs, assets, payroll, loans, etc.)",
    value="Craft beer bar selling draft beer, snacks, merch; uses Square POS; has inventory; payroll; rent; tips.",
    height=140
)

uploaded_pdf = st.file_uploader("Optional: Upload bank statement PDF", type=["pdf"])

evidence = None
if uploaded_pdf is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.getbuffer())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path, max_pages=3)
    evidence = build_evidence_pack_from_pdf_text(text)

    st.subheader("What I detected (MVP)")
    st.write({"hints": evidence.hints, "top_vendors": evidence.top_vendors})
    os.unlink(tmp_path)

out_name = st.text_input("Output filename", value="Chart_of_Accounts.xlsx")

if st.button("Generate Excel"):
    hints = evidence.hints if evidence else []
    top_vendors = evidence.top_vendors if evidence else []
    raw_excerpt = evidence.raw_text_excerpt if evidence else ""

    run(
        entity_type=entity_type,
        entity_name=entity_name,
        description=description,
        out_path=out_name,
        hints=hints,
        top_vendors=top_vendors,
        raw_excerpt=raw_excerpt,
    )

    with open(out_name, "rb") as f:
        st.success("Done!")
        st.download_button(
            label="Download Chart of Accounts (Excel)",
            data=f,
            file_name=out_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
