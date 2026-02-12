import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import pandas as pd
    import marimo as mo
    import duckdb

    return duckdb, os


@app.cell
def _(os):
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "listings.db")
    return (DB_PATH,)


@app.cell
def _(DB_PATH, duckdb):
    with duckdb.connect(DB_PATH) as con:
        con.sql(f"""
            SELECT * 
            FROM raw_listings
            LIMIT 5
            ;
        """).show()
    return


if __name__ == "__main__":
    app.run()
