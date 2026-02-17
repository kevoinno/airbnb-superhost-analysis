import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Overview

    This script is used to setup the persistent DuckDB database by combining the data from all the 2025 months in NYC together.

    Once this script runs and the database is established, we can interact with the database using a connection. **This means we only have to run this script once to populate our DuckDB database.**
    """)
    return


@app.cell
def _():
    import os
    import pandas as pd
    import marimo as mo
    import duckdb

    return duckdb, mo, os


@app.cell
def _(os):
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "listings_*.csv.gz")
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "listings.db")
    return DATA_PATH, DB_PATH


@app.cell
def _(DATA_PATH, DB_PATH, duckdb):
    with duckdb.connect(DB_PATH) as con:
        con.sql(f"""
            CREATE OR REPLACE TABLE raw_listings AS
            SELECT 
                *,
                last_scraped::DATE AS snapshot_date, -- Automatically extract the date from the data itself
                filename AS source_file -- Keep the filename as a backup identifier
            FROM read_csv_auto(
                '{DATA_PATH}', 
                filename=True, 
                union_by_name=True
            )
        """)
        print("Database Load Complete.")
    return


if __name__ == "__main__":
    app.run()
