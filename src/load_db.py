"""
load_db.py
Loads cleaned job postings data into a local SQLite database
so it can be queried with SQL for analysis.
"""

import sqlite3
import pandas as pd


def create_connection(db_path: str) -> sqlite3.Connection:
    """Create (or connect to) a SQLite database file."""
    return sqlite3.connect(db_path)


def load_dataframe_to_db(df: pd.DataFrame, conn: sqlite3.Connection, table_name: str = "job_postings") -> None:
    """
    Write a cleaned DataFrame into a SQLite table.
    Replaces the table if it already exists (useful for re-runs).

    Args:
        df: cleaned, validated DataFrame.
        conn: active SQLite connection.
        table_name: name of the table to create/replace.
    """
    df.to_sql(table_name, conn, if_exists="replace", index=False)


def sanity_check(conn: sqlite3.Connection, table_name: str = "job_postings") -> None:
    """Print row count from the DB table to confirm the load worked."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Rows loaded into '{table_name}': {count}")


if __name__ == "__main__":
    CLEANED_CSV = "data/cleaned_jobs.csv"
    DB_PATH = "data/job_postings.db"

    cleaned_df = pd.read_csv(CLEANED_CSV)

    conn = create_connection(DB_PATH)
    load_dataframe_to_db(cleaned_df, conn)
    sanity_check(conn)
    conn.close()

    print(f"\nDatabase ready at {DB_PATH}")