"""
ingest.py
Loads the raw job postings CSV and prints basic inspection info.
This is the entry point of the pipeline: CSV -> pandas DataFrame.
"""

import pandas as pd


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load the raw job postings CSV into a DataFrame.

    Args:
        filepath: path to the raw CSV file.

    Returns:
        Raw, unmodified DataFrame.
    """
    df = pd.read_csv(filepath)
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """
    Print basic diagnostics about the raw dataset:
    shape, column names, null counts, and duplicate count.
    Used to decide what cleaning steps are needed.
    """
    print("=" * 50)
    print("RAW DATA INSPECTION")
    print("=" * 50)
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nColumns:\n{list(df.columns)}")
    print(f"\nNull values per column:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print("=" * 50)


if __name__ == "__main__":
    RAW_PATH = "data/fake_job_postings.csv"  # adjust filename if different

    raw_df = load_raw_data(RAW_PATH)
    inspect_data(raw_df)