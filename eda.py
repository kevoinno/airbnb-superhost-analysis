import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    import pandas as pd
    import numpy as np
    import os

    return PercentFormatter, duckdb, mo, np, os, plt


@app.cell
def _(os):
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'listings.db')
    return (DB_PATH,)


@app.cell
def _(DB_PATH, duckdb):
    # grab data from duckdb database (mart is already host-level, one row per host)
    with duckdb.connect(DB_PATH) as con:
        hosts = con.sql("SELECT * FROM listings_fuzzy_rdd").df()
    return (hosts,)


@app.cell
def _(hosts):
    print(f"Number of hosts: {hosts.shape[0]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Questions
    1. How many and what proportion of hosts qualify for superhost based on overall rating?
    2. How many and what proportion of hosts qualify for superhost based on response rate?
    3. Distributions of overall rating and response rate? How many NA for each?
    """)
    return


@app.cell
def _(PercentFormatter, np, plt):
    # distributions
    def relative_hist(data, title):
        fig, ax = plt.subplots()
    
        ax.hist(data,
                 weights = np.ones(data.shape[0]) / data.shape[0] * 100, 
                 bins = 50, edgecolor = "black");
        ax.set_title(title);
        ax.yaxis.set_major_formatter(PercentFormatter())
    
        return fig, ax

    return (relative_hist,)


@app.cell
def _(relative_hist, hosts):
    # overall ratings
    rating_fig, rating_ax = relative_hist(hosts['avg_host_review_score'], "Distribution of Overall Host Ratings")
    rating_ax.vlines(x = 4.8, ymin = 0, ymax = 30, color = 'red', linestyle='--')
    rating_fig
    return


@app.cell
def _(relative_hist, hosts):
    # response rate
    response_fig, response_ax = relative_hist(hosts['host_response_rate'], "Distribution of Host Response Rate")
    response_ax.vlines(x = 90, ymin = 0, ymax = 50, color = 'red', linestyle='--')
    response_fig
    return


@app.cell
def _(hosts):
    # percent of NA values
    (hosts[['avg_host_review_score', 'host_response_rate']].isna().sum() / hosts.shape[0] * 100).reset_index(name = 'perc_NA')
    return


@app.cell
def _(hosts):
    # percent of failing users due to each criteria
    num_below_rating = hosts[hosts['avg_host_review_score'] < 4.8].shape[0]
    num_below_response = hosts[hosts['host_response_rate'] < 90].shape[0] 
    print(f"People failing by overall rating: {num_below_rating} ({num_below_rating / hosts.shape[0] * 100:.2f})%\n")
    print(f"People failing by response rate: {num_below_response} ({num_below_response / hosts.shape[0] * 100:.2f})%\n")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will argue that having the overall rating being at least 4.8 will be the running variable because:
    - More hosts fail to meet this criteria compared to the response rating
    - Almost half of the hosts have an NA response rate
    """)
    return


if __name__ == "__main__":
    app.run()
