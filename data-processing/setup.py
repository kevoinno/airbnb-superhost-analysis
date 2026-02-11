import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Overview

    This script is used to setup the persistent DuckDB database by combining the data from all the 2025 months in NYC together.

    Once this script runs and the database is established, we can interact with the database using a connection. **This means we only have to run this script once to populatie our DuckDB database.**
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
    DATA_PATH = os.path.join("..", "data", "listings_dec_2025.csv")
    DB_PATH = os.path.join("..", "data", "listings.db")
    return DATA_PATH, DB_PATH


@app.cell
def _(DATA_PATH, DB_PATH, duckdb):
    with duckdb.connect(DB_PATH) as con:
        con.sql(f"""
        DESCRIBE-
        SELECT *
        FROM '{DATA_PATH}'
        """).show()
    
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Questions
    1. How do all the criteria apply to a person with many listings?
    2. What is a good proxy for cancellation rate?
    3. Is the overall rating a rating for the host or the property?
    4. How do we know if a review counts towards Superhost status?
        - Would we have to manually sift through all the reviews to determine if it counts toward an assessment period?
    5. Since there are multiple assessment periods in a year, how would we handle people that lost and earned the Superhost badge throughout the year.
    6. How do we handle multiple hosts showing up in multiple quarters where their status of Superhost can change?
    """)
    return


if __name__ == "__main__":
    app.run()
