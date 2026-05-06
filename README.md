# Supplier Scorecard Dashboard

A small Streamlit dashboard for reviewing supplier performance from the generated scorecard output.

## What it shows

The dashboard summarizes:
- on-time delivery rate
- average lead time
- defect rate
- cost savings
- compliance rate
- weighted supplier score

## How it is calculated

- on-time delivery rate = delivered orders with delivery time <= 30 days / total delivered orders
- average lead time = average days between order date and delivery date
- defect rate = defective units / total ordered units
- cost savings = average of (unit price - negotiated price) / unit price
- compliance rate = compliant orders / total orders
- weighted supplier score = 35% OTD + 25% quality + 20% compliance + 10% savings + 10% lead time efficiency

The dashboard also shows a normalized comparison view where higher is better for quality, compliance, savings, and lead time efficiency.

## How to run

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Data

The dashboard reads from `output/scorecard_results.csv`.

If you want to regenerate the scorecard, use the SQL scripts in `sql/` against the source data in `database/`.
