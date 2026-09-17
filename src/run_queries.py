"""
run_queries.py
Runs each query in sql/queries.sql against the SQLite database
and prints/saves the results.
"""

import sqlite3
import pandas as pd


def run_all_queries(db_path: str, sql_file: str, output_md: str) -> None:
    conn = sqlite3.connect(db_path)

    with open(sql_file, "r") as f:
        content = f.read()

    # Split on the '-- N.' comment markers to get individual queries
    raw_queries = [q.strip() for q in content.split(";") if q.strip() and "SELECT" in q.upper()]

    results_md = ["# SQL Query Results\n"]

    for i, query in enumerate(raw_queries, start=1):
        print(f"\n--- Query {i} ---")
        try:
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))
            results_md.append(f"## Query {i}\n```sql\n{query.strip()}\n```\n")
            results_md.append(df.to_markdown(index=False) + "\n")
        except Exception as e:
            print(f"Error running query {i}: {e}")

    conn.close()

    with open(output_md, "w") as f:
        f.write("\n".join(results_md))
    print(f"\nSaved all results to {output_md}")


if __name__ == "__main__":
    run_all_queries(
        db_path="data/job_postings.db",
        sql_file="sql/queries.sql",
        output_md="sql/results.md",
    )