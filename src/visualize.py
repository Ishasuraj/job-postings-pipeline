"""
visualize.py
Generates a bar chart showing fraud rate by employment type,
pulled directly from the SQLite database, and saves it as a PNG
for inclusion in the README.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def get_fraud_by_employment_type(db_path: str) -> pd.DataFrame:
    """Query fraud rate by employment type from the SQLite database."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT
            employment_type,
            COUNT(*) AS total_postings,
            SUM(fraudulent) AS fraud_count,
            ROUND(100.0 * SUM(fraudulent) / COUNT(*), 2) AS fraud_rate_pct
        FROM job_postings
        WHERE employment_type != ''
        GROUP BY employment_type
        ORDER BY fraud_rate_pct DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def plot_fraud_rate(df: pd.DataFrame, output_path: str) -> None:
    """Create and save a bar chart of fraud rate by employment type."""
    plt.figure(figsize=(9, 5))
    bars = plt.bar(df["employment_type"], df["fraud_rate_pct"], color="#c0392b")

    plt.title("Fraud Rate by Employment Type", fontsize=14, fontweight="bold")
    plt.xlabel("Employment Type")
    plt.ylabel("Fraud Rate (%)")
    plt.xticks(rotation=20)

    # Label each bar with its value
    for bar, value in zip(bars, df["fraud_rate_pct"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{value}%",
            ha="center",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved chart to {output_path}")


if __name__ == "__main__":
    DB_PATH = "data/job_postings.db"
    OUTPUT_PATH = "plots/fraud_by_employment_type.png"

    data = get_fraud_by_employment_type(DB_PATH)
    print(data)

    plot_fraud_rate(data, OUTPUT_PATH)
