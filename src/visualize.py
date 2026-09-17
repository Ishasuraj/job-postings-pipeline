"""
visualize.py
Create a simple chart summarizing fraud rate by employment type.
"""

import os
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def get_fraud_by_employment_type(db_path: str) -> pd.DataFrame:
    """Query the SQLite database for fraud rate by employment type."""
    query = """
        SELECT
            employment_type,
            COUNT(*) AS total_postings,
            SUM(fraudulent) AS fraud_count,
            ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
        FROM job_postings
        WHERE employment_type != ''
        GROUP BY employment_type
        ORDER BY fraud_rate_pct DESC
    """

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def save_chart(df: pd.DataFrame, output_path: str) -> None:
    """Render a bar chart and save it to a PNG file."""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    colors = ["#2E86C1", "#1ABC9C", "#F5B041", "#D35400", "#7D3C98"]

    plt.bar(df["employment_type"], df["fraud_rate_pct"], color=colors[: len(df)])
    plt.title("Fraud Rate by Employment Type")
    plt.xlabel("Employment Type")
    plt.ylabel("Fraud Rate (%)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    db_path = "data/job_postings.db"
    output_path = "plots/fraud_by_employment_type.png"

    df = get_fraud_by_employment_type(db_path)
    save_chart(df, output_path)
    print(f"Saved chart to {output_path}")
