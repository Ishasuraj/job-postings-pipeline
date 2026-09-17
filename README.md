# Job Postings Fraud Analytics Pipeline

A Python data pipeline that ingests, cleans, validates, and analyzes job posting data to surface patterns associated with fraudulent listings — built to strengthen hands-on SQL, data validation, and testing skills.

## Architecture

```
Raw CSV → Python (clean + validate) → SQLite → SQL Analysis → Visualization
```

## What It Does

1. **Ingests** ~17,880 job postings from the [Kaggle Fake Job Postings dataset](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)
2. **Cleans and validates** each record — normalizing text fields, checking for required data, and flagging malformed entries (e.g. non-numeric salary ranges)
3. **Loads** the validated data into a local SQLite database
4. **Analyzes** it with SQL — including aggregations, correlations, and a window-function ranking
5. **Visualizes** key findings as a chart
6. **Tests** the validation logic with pytest

## Key Findings

- Overall fraud rate across the dataset: **4.83%**
- Postings with **no company logo** have a fraud rate of **15.76%** — nearly 8x higher than postings with a logo (2.00%)
- **Oil & Energy** is the highest-risk industry by fraud rate at **37.54%**
- **Part-time** roles have the highest fraud rate among employment types (**9.45%**)
- **Remote/telecommuting** postings show a higher fraud rate (**8.45%**) than on-site postings (**4.67%**)

![Fraud rate by employment type](plots/fraud_by_employment_type.png)

## Data Quality

- Raw rows ingested: 17,880
- Duplicates removed: 0
- Rows failed validation: 346 (missing location, invalid salary format, etc.)
- Final clean rows loaded: **17,534**

Full breakdown in [`data_quality_report.md`](data_quality_report.md).

## Tech Stack

Python, pandas, SQLite, pytest, matplotlib, Git

## SQL Highlights

7 queries in [`sql/queries.sql`](sql/queries.sql), including:
- Fraud rate by employment type, industry, and required experience
- Company logo and telecommuting correlation with fraud
- A window-function query ranking industries by fraud rate (`RANK() OVER (...)`)

Full results in [`sql/results.md`](sql/results.md).

## Testing

5 unit tests covering the row-validation logic (valid input, missing fields, invalid flags, malformed salary format):

```
pytest tests/test_validation.py
```

## Cloud Migration Note

Analysis was initially planned for Google Cloud BigQuery. GCP required a one-time prepayment for billing verification on this account (an India-specific requirement, separate from trial credits), so analysis was kept local in SQLite instead. The SQL used is standard and portable to BigQuery or AWS Athena with minimal changes.

## How to Run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Download the dataset from Kaggle and place it at data/fake_job_postings.csv

python src/ingest.py
python src/clean.py
python src/load_db.py
python src/run_queries.py
python src/visualize.py
pytest tests/test_validation.py
```

## Future Work

- Migrate analysis to a cloud data warehouse (BigQuery / AWS Athena)
- Expand unit test coverage to the cleaning pipeline itself
- Add a CI workflow to run tests automatically on push
