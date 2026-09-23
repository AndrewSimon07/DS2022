#!/usr/bin/env python3
"""Load a CSV into a local DuckDB database (Lab 04 optional Step 8).

Requires:
  uv add pandas duckdb

Put MOCK_DATA.csv in the current directory, then:
  uv run python duckdb_example.py

Creates mock.duckdb in the current directory with a table named mock.
"""

import duckdb
import pandas as pd

CSV_FILE = "MOCK_DATA.csv"
DB_FILE = "mock.duckdb"
TABLE = "mock"


def main():
    """Read CSV, drop incomplete rows, and write them into a DuckDB file."""
    df = pd.read_csv(CSV_FILE)
    df = df.dropna()
    print(f"Loaded {len(df)} rows from {CSV_FILE} after dropna()")

    con = duckdb.connect(DB_FILE)
    try:
        # DuckDB can create a table directly from a pandas DataFrame
        con.execute(f"CREATE OR REPLACE TABLE {TABLE} AS SELECT * FROM df")
        count = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
        sample = con.execute(f"SELECT * FROM {TABLE} LIMIT 5").fetchdf()
        print(f"Wrote {count} rows to {DB_FILE} table '{TABLE}'")
        print(sample)
    finally:
        con.close()


if __name__ == "__main__":
    main()
