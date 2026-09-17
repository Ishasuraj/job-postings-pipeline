"""
clean.py
Cleans raw job posting data and validates each row.
Cleaning fixes the data; validation checks it.
Kept as separate functions so validation can be unit tested in isolation.
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Clean the raw job postings DataFrame:
    - drop exact duplicate rows
    - fill missing text fields with empty string
    - standardize text casing/whitespace on key columns

    Args:
        df: raw DataFrame from ingest.py

    Returns:
        A tuple of (cleaned DataFrame, stats dict) where stats records
        row counts at each step for the data quality report.
    """
    stats = {"raw_rows": len(df)}

    # Drop duplicates
    df = df.drop_duplicates()
    stats["duplicates_removed"] = stats["raw_rows"] - len(df)

    # Standardize key text columns if present
    text_cols = ["title", "location", "employment_type", "required_experience"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

    # Fill remaining nulls in object columns with empty string
    obj_cols = df.select_dtypes(include="object").columns
    df[obj_cols] = df[obj_cols].fillna("")

    # Ensure fraudulent flag is numeric (0/1) if present
    if "fraudulent" in df.columns:
        df["fraudulent"] = pd.to_numeric(df["fraudulent"], errors="coerce").fillna(0).astype(int)

    stats["clean_rows"] = len(df)
    return df, stats


def validate_row(row: dict) -> bool:
    """
    Check whether a single job posting row meets minimum data quality rules.

    Rules:
    - 'title' must be non-empty
    - 'location' must be non-empty
    - 'fraudulent' must be 0 or 1 if present

    Args:
        row: a dict representing one row (e.g. from df.to_dict('records')).

    Returns:
        True if the row passes all checks, False otherwise.
    """
    title = str(row.get("title", "")).strip()
    location = str(row.get("location", "")).strip()

    if not title:
        return False
    if not location:
        return False

    fraudulent = row.get("fraudulent", 0)
    if fraudulent not in (0, 1):
        return False

    salary_range = row.get("salary_range", "")
    if salary_range:
        import re
        # Expect a format like "$90,000 - $110,000" or "90000-110000"
        if not re.search(r"\d", str(salary_range)):
            return False

    return True


def validate_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Apply validate_row() across the full DataFrame.

    Returns:
        A tuple of (only the valid rows, count of rows that failed validation).
    """
    records = df.to_dict("records")
    valid_mask = [validate_row(r) for r in records]
    failed_count = valid_mask.count(False)
    valid_df = df[valid_mask].reset_index(drop=True)
    return valid_df, failed_count


if __name__ == "__main__":
    from ingest import load_raw_data

    raw_df = load_raw_data("data/fake_job_postings.csv")
    cleaned_df, stats = clean_data(raw_df)
    final_df, failed_count = validate_dataframe(cleaned_df)

    stats["failed_validation"] = failed_count
    stats["final_rows"] = len(final_df)

    print("DATA QUALITY REPORT")
    print(f"Raw rows: {stats['raw_rows']}")
    print(f"Duplicates removed: {stats['duplicates_removed']}")
    print(f"Rows failed validation: {stats['failed_validation']}")
    print(f"Final clean rows: {stats['final_rows']}")

    # Save cleaned + validated data for load_db.py
    final_df.to_csv("data/cleaned_jobs.csv", index=False)
    print("\nSaved cleaned data to data/cleaned_jobs.csv")

    # Save quality report
    with open("data_quality_report.md", "w") as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"- Raw rows: {stats['raw_rows']}\n")
        f.write(f"- Duplicates removed: {stats['duplicates_removed']}\n")
        f.write(f"- Rows failed validation: {stats['failed_validation']}\n")
        f.write(f"- Final clean rows: {stats['final_rows']}\n")
    print("Saved data_quality_report.md")