## Airbnb Superhost Analysis Overview

Have you thought about being an Airbnb host? While booking properties, you might have seen a cool title for experienced, excellent hosts called "Superhost". To get this title, you have to meet several criteria, and this analysis attempts to quantify the value of having this title for your business.

## Identification Strategy 

The main question is "What is the effect of having Superhost status on bookings for the host's listings?"

I attempted to answer this question using a Fuzzy Regression Discontinuity Design.

For the analysis, I used the following variables:
- Avg Review Score Rating of the host (X)
- Whether they qualified based on their avg review score (Z)

When a the review score rating meets the cutoff of 4.8, the host is **encouraged** to receive to a Superhost badge, but it isn't guaranteed.

- Presence of Superhost badge on the listing (D)
- Number of reviews in the last 12 months for the listing (a proxy for bookings) (Y)

The granularity of the data will be on the listings level because the outcome variable is the number of bookings in the last 12 months for each listing.

TODO:

### Planning
- Understand the logic of IV and apply to it the Fuzzy RDD DAG
- Figure out how Fuzzy RDD will work and list out assumptions (don't need to defend for now)
- Figure out how to get to the correct granularity
- Draw a DAG to show how this works

### Data Processing
- Load all data into a DuckDB db in load.py
- Get data into correct form using dbt (after planning)

Final form of data
- Feb and Jan 2025 are missing 
- all in duckdb
- raw data will not be on Github




