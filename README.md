# Chart of Accounts Model (LLM → Excel)

Describe an entity and generate a tailored Chart of Accounts (2-column Excel).

## Setup

Clone the repository:

```bash
git clone https://github.com/GarrettOlitsky/coa-model.git
cd coa-model
Create and activate a virtual environment:

bash
Copy code
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
yaml
Copy code

That’s it. Clean and standard.

---

## Optional (but nice): add a “Run” section

Right after Setup, add:

```md
## Run (CLI)

Generate a Chart of Accounts from a plain-English description:

```bash
python -m src.main \
  --type for-profit \
  --name "REGAL ALE" \
  --out "Chart_of_Accounts.xlsx" \
  --desc "Craft beer bar selling draft beer, snacks, merch; uses Square POS; has inventory; payroll; rent; tips."
Run (Streamlit UI)
bash
Copy code
streamlit run app.py
