# Supplier Scorecard

A small Streamlit dashboard for reviewing supplier performance from the generated scorecard output.

## What it shows

The dashboard summarizes:
- on-time delivery rate
- average lead time
- defect rate
- cost savings
- compliance rate
- weighted supplier score

## How to run

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Data

The dashboard reads from `output/scorecard_results.csv`.

If you want to regenerate the scorecard, use the SQL scripts in `sql/` against the source data in `database/`.
