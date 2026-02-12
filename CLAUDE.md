# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Econometric analysis of Airbnb Superhost status effects on bookings using a Fuzzy Regression Discontinuity Design. Data comes from Inside Airbnb (NYC listings). The running variable is average review score rating (cutoff: 4.8), and the outcome is number of reviews in the last 12 months (proxy for bookings).

## Setup & Commands

- **Python**: 3.13 (managed via `uv`)
- **Install dependencies**: `uv sync`
- **Run marimo notebooks**: `uv run marimo edit <notebook.py>` (opens in browser)
- **Run marimo as script**: `uv run python <notebook.py>`

## Architecture

- `data-processing/` — Marimo notebook scripts for ETL. Run from this directory (paths are relative to it).
  - `setup.py` — Marimo notebook that loads CSV data into a persistent DuckDB database at `data/listings.db`
- `data/` — Raw CSVs and DuckDB database (not committed to git). Files follow the naming convention `listings_<month>_<year>.csv`.
- DuckDB is the primary data store; raw CSVs are loaded once via `setup.py`, then all subsequent analysis queries the `.db` file.

## Key Dependencies

- **duckdb** — Analytical database for all data storage and querying
- **marimo** — Reactive notebook framework (scripts are `.py` files with `@app.cell` decorators)
- **pandas** — Data manipulation
