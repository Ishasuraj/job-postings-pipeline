# Project Status: Job Postings Fraud Analytics Pipeline

## Overview
This project builds a data pipeline for analyzing fake or suspicious job postings. The workflow includes ingestion, cleaning, validation, database loading, SQL analysis, visualization, and testing.

## Completed Work

### Phase 0: Setup
- Created the repository structure for the pipeline.
- Initialized Git and created the first commit.
- Added project-level ignore rules in `.gitignore`.
- Established the project folders:
  - `data/`
  - `src/`
  - `sql/`
  - `tests/`

### Phase 1: Ingestion
- Implemented `src/ingest.py` to load the raw CSV into a pandas DataFrame.
- Added a basic inspection function to print:
  - row and column count
  - column names
  - null counts per column
  - duplicate count

### Phase 2: Cleaning + Validation
- Implemented `src/clean.py` with:
  - duplicate removal
  - whitespace and casing normalization for key text fields
  - null handling for text columns
  - conversion of the `fraudulent` flag to numeric 0/1 values
- Added a separate `validate_row(row)` function for validating individual records.
- Added validation tests in `tests/test_validation.py`.
- Confirmed the validation logic passes multiple checks, including malformed salary rejection.

### Phase 3: Load into SQLite
- Implemented `src/load_db.py` to:
  - create or connect to a SQLite database
  - write cleaned data to a table
  - print a row-count sanity check
- The cleaned data has been loaded and stored in `data/job_postings.db`.

### Phase 4: SQL Analysis
- Added analytical queries in `sql/queries.sql` covering:
  - fraud rate by employment type
  - fraud rate by required experience
  - industries by posting volume and fraud rate
  - company logo correlation with fraud
  - telecommuting versus fraud rate
  - overall fraud summary
- Executed the queries with `src/run_queries.py`.
- Saved the output results in `sql/results.md`.

### Phase 5: BigQuery Migration
- This was planned for later migration, and the project structure supports it.
- The repo is prepared to export cleaned data and import into BigQuery for follow-up analysis.

### Phase 6: Data Quality Reporting
- Added print/logging output in `clean.py` for the data quality report.
- Saved the final quality metrics in `data_quality_report.md`.

Current report summary:
- Raw rows: 17,880
- Duplicates removed: 0
- Rows failed validation: 346
- Final clean rows: 17,534

### Phase 7: Visualization
- Added `src/visualize.py` to create a fraud-rate chart from the SQLite data.
- Generated a visualization in `plots/fraud_by_employment_type.png`.
- The output image is referenced from the README.

### Phase 8: Unit Tests
- Added a pytest suite in `tests/test_validation.py`.
- The test suite currently passes.

Current test result:
- 5 passed

## Current Repository Artifacts
- `.gitignore`
- `README.md`
- `PROJECT_STATUS.md`
- `data_quality_report.md`
- `data/fake_job_postings.csv`
- `data/cleaned_jobs.csv`
- `data/job_postings.db`
- `sql/queries.sql`
- `sql/results.md`
- `src/ingest.py`
- `src/clean.py`
- `src/load_db.py`
- `src/run_queries.py`
- `src/visualize.py`
- `tests/test_validation.py`
- `plots/fraud_by_employment_type.png`

## Key Insight
One of the clearest patterns in the project data is that certain employment types and job characteristics are associated with a higher fraud rate, making the data useful for identifying suspicious postings.

## Next Recommended Steps
- Finalize the BigQuery migration section and results export.
- Add a more polished README for portfolio presentation.
- Commit the final project documentation and generated outputs.
- Consider adding a production-ready CI/test workflow.
