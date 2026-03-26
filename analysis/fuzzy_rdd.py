import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt
    import duckdb
    import os
    from rdrobust import rdrobust, rdbwselect, rdplot

    return duckdb, mo, os, plt, rdrobust


@app.cell
def _(duckdb, os):
    # load data
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'listings.db')

    with duckdb.connect(DB_PATH) as con:
        listings_rdd = con.sql("""
        SELECT * 
        FROM listings_fuzzy_rdd
        ;
        """).df()
    return (listings_rdd,)


@app.cell
def _(listings_rdd):
    # center overall rating cutoff
    def center_overall_ratings(df):
        # center around 4.8
        df['centered_overall_score'] =  df['avg_host_review_score'] - 4.8
        return df

    centered_listings_rdd = (listings_rdd.pipe(center_overall_ratings))
    return (centered_listings_rdd,)


@app.cell
def _():
    # plot overall score vs number of reviews in last 12 months
    return


@app.cell
def _(centered_listings_rdd, plt):
    # run McCrary Test
    fig, ax = plt.subplots()

    ax.hist(x = centered_listings_rdd['centered_overall_score'],
            bins = 100,
            density = True,
            edgecolor = "black")
    ax.set_title("McCrary Test")

    fig
    return


@app.cell
def _(centered_listings_rdd, rdrobust):
    # run RDD model
    rdd_result = rdrobust(
        y          = centered_listings_rdd['num_reviews_l12m'],
        x          = centered_listings_rdd['centered_overall_score'],
        fuzzy      = centered_listings_rdd['has_superhost'],  # specify fuzzy design
        masspoints = "adjust",
        all = True
    )
    rdd_result
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The robust results show that we are 95% confident that for the hosts who when crossing the 4.8 overall rating threshold, would have received superhost status, the effect becoming superhost would have increased their number of review somewhere between 20 and 165. Since number of reviews is some proxy for bookings, this effect could lead to even more bookings.
    """)
    return


@app.cell
def _():
    # Fuzzy RDD idea
    # outcome ~ running*treatement --> LATE in Sharp Design
    # 
    # 
    # Problem
    # Y_1 appears smaller than it should be because some people over the threshold are not treated
    # Y_0 appears larger than it should be because some people under the threshold are treated
    # --> Effect is underestimated
    # 
    # Threshold (0 or 1) acts as an instrumental variable and we do an IV like regression
    # 1st stage: D ~ Z*R
    # reduced form: Y ~ Z*R
    # LATE: reduce / 1st stage
    return


if __name__ == "__main__":
    app.run()
