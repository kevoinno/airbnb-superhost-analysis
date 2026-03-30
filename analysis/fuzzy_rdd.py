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
    import numpy as np
    from rdrobust import rdrobust, rdbwselect, rdplot

    return duckdb, mo, np, os, plt, rdplot, rdrobust


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
def _(centered_listings_rdd, np, plt):
    # Exploratory RDD plot: outcome vs running variable
    # Bins the centered score and plots mean reviews per bin,
    # with local linear fits on each side to show the discontinuity visually.
    _cutoff = 0
    _df = centered_listings_rdd[['centered_overall_score', 'num_reviews_l12m']].dropna()
    _x = _df['centered_overall_score'].values
    _y = _df['num_reviews_l12m'].values

    # Bin means
    _nbins = 40
    _bins = np.linspace(_x.min(), _x.max(), _nbins + 1)
    _bin_centers = (_bins[:-1] + _bins[1:]) / 2
    _bin_means = [_y[(_x >= _bins[i]) & (_x < _bins[i+1])].mean() for i in range(_nbins)]
    _bin_means = np.array(_bin_means)
    _valid = ~np.isnan(_bin_means)

    _left  = _bin_centers < _cutoff
    _right = _bin_centers >= _cutoff

    # Local linear fit on each side
    def _ll_fit(xc, yc):
        X = np.column_stack([np.ones_like(xc), xc])
        return np.linalg.lstsq(X, yc, rcond=None)[0]

    _bl = _ll_fit(_bin_centers[_left  & _valid], _bin_means[_left  & _valid])
    _br = _ll_fit(_bin_centers[_right & _valid], _bin_means[_right & _valid])

    _xs_l = np.linspace(_x.min(), _cutoff, 200)
    _xs_r = np.linspace(_cutoff, _x.max(), 200)

    fig_rdd_explore, _ax = plt.subplots()
    _ax.scatter(_bin_centers[_left  & _valid], _bin_means[_left  & _valid], color='steelblue', s=20, zorder=3)
    _ax.scatter(_bin_centers[_right & _valid], _bin_means[_right & _valid], color='tomato',    s=20, zorder=3)
    _ax.plot(_xs_l, _bl[0] + _bl[1] * _xs_l, color='steelblue')
    _ax.plot(_xs_r, _br[0] + _br[1] * _xs_r, color='tomato')
    _ax.axvline(_cutoff, color='black', linestyle='--', linewidth=1)
    _ax.set_title("Reviews (last 12m) by centered overall score")
    _ax.set_xlabel("Centered overall score  (0 = 4.8 cutoff)")
    _ax.set_ylabel("Avg reviews (last 12m)")
    fig_rdd_explore
    return


@app.cell
def _(centered_listings_rdd, np, plt):
    from scipy import stats as _stats

    # McCrary (2008) density discontinuity test
    # Bins the running variable, fits local linear regressions on each side,
    # tests for a jump in density at the cutoff.
    # p > 0.05 = no evidence of sorting / score manipulation.

    score = centered_listings_rdd['centered_overall_score'].dropna().values
    cutoff = 0
    n = len(score)

    # Bin width: McCrary (2008) default = 2*sd*n^{-1/2}
    bin_width = 2 * np.std(score) * n**(-1/2)
    bins = np.arange(score.min(), score.max() + bin_width, bin_width)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    counts, _ = np.histogram(score, bins=bins)
    density = counts / (n * bin_width)

    # Bandwidth for local linear fit: 2*sd*n^{-1/5} (plug-in)
    bw = 2 * np.std(score) * n**(-1/5)

    left  = bin_centers < cutoff
    right = bin_centers >= cutoff

    def tri_kernel(x, h):
        return np.maximum(1 - np.abs(x) / h, 0)

    def wls_local_linear(X, Y, W):
        """Fit intercept + slope via WLS; return intercept estimate and its SE."""
        mask = W > 0
        X, Y, W = X[mask], Y[mask], W[mask]
        Xmat = np.column_stack([np.ones_like(X), X])
        WXX  = (Xmat.T * W) @ Xmat
        WXY  = (Xmat.T * W) @ Y
        beta = np.linalg.solve(WXX, WXY)
        resid = Y - Xmat @ beta
        sigma2 = np.sum(W * resid**2) / (len(Y) - 2)
        var_beta = sigma2 * np.linalg.inv(WXX)
        return beta[0], np.sqrt(var_beta[0, 0])

    Xl = bin_centers[left]  - cutoff
    Xr = bin_centers[right] - cutoff

    Wl = tri_kernel(Xl, bw)
    Wr = tri_kernel(Xr, bw)

    f_minus, se_minus = wls_local_linear(Xl, density[left],  Wl)
    f_plus,  se_plus  = wls_local_linear(Xr, density[right], Wr)

    jump    = f_plus - f_minus
    se_jump = np.sqrt(se_minus**2 + se_plus**2)
    t_stat  = jump / se_jump
    p_value = 2 * _stats.norm.sf(abs(t_stat))

    print("McCrary Density Test")
    print(f"  Density left of cutoff:  {f_minus:.4f}  (SE {se_minus:.4f})")
    print(f"  Density right of cutoff: {f_plus:.4f}  (SE {se_plus:.4f})")
    print(f"  Jump at cutoff:          {jump:.4f}  (SE {se_jump:.4f})")
    print(f"  T-statistic:             {t_stat:.3f}")
    print(f"  P-value:                 {p_value:.4f}")

    # Plot: binned density + fitted local linear curves
    def ll_predict(xs, X_fit, Y_fit, W_fit, h):
        """Evaluate local linear fit at each point in xs."""
        preds = []
        for x in xs:
            w = tri_kernel(X_fit - x, h)
            if w.sum() == 0:
                preds.append(np.nan)
                continue
            Xm = np.column_stack([np.ones(len(X_fit)), X_fit - x])
            beta = np.linalg.solve((Xm.T * w) @ Xm, (Xm.T * w) @ Y_fit)
            preds.append(beta[0])
        return np.array(preds)

    xs_l = np.linspace(bin_centers[left].min(),  cutoff, 200)
    xs_r = np.linspace(cutoff, bin_centers[right].max(), 200)

    fig_density, _ax = plt.subplots()
    _ax.scatter(bin_centers[left],  density[left],  color='steelblue', s=10, alpha=0.7)
    _ax.scatter(bin_centers[right], density[right], color='tomato',    s=10, alpha=0.7)
    _ax.plot(xs_l, ll_predict(xs_l - cutoff, Xl, density[left],  Wl, bw), color='steelblue', label='Left of cutoff')
    _ax.plot(xs_r, ll_predict(xs_r - cutoff, Xr, density[right], Wr, bw), color='tomato',    label='Right of cutoff')
    _ax.axvline(cutoff, color='black', linestyle='--', linewidth=1)
    _ax.set_title(f"McCrary Density Test  |  T = {t_stat:.3f},  p = {p_value:.3f}")
    _ax.set_xlabel("Centered overall score")
    _ax.set_ylabel("Density")
    _ax.legend()
    fig_density
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $H_0$: The density of centered scores is continuous at the cutoff (no evidence of sorting)
    $H_1$: The density of centered scores is discontinuous at the cutoff (evidence of sorting)

    In this case, there is not enough evidence to say that there sorting going on. Sorting means that hosts are tweaking their scores to be slighlty above or below the cutoff to manipulate whether they get superhost status or not.

    For this example, we can assume that hosts are not purposefully decreasing their overall rating to not get super host, since lower ratings also affects their bookings. The McCrary Test also shows that there is not enough evidence to say that they were artifically inflating their scores to meet the cutoff and increase their chances of becoming a superhost.
    """)
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
    return (rdd_result,)


@app.cell
def _(centered_listings_rdd, rdd_result, rdplot):
    # rdplot: visualise the fit using the same bandwidth as the estimated model
    # Shows the polynomial fit and binned means on each side of the cutoff
    rdplot(
        y          = centered_listings_rdd['num_reviews_l12m'].to_numpy().copy(),
        x          = centered_listings_rdd['centered_overall_score'].to_numpy().copy(),
        h          = rdd_result.bws.iloc[0].tolist(),   # MSE-optimal bandwidth from rdrobust
        masspoints = "adjust",
    )
    return


@app.cell
def _(rdd_result):
    rdd_result.bws
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
