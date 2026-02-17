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

### **Causal Estimand**
  We will be trying to estimate the **Local Average Treatment Effect** - the effect of having the Superhost badge on number of reviews in the last 12 months for hosts whose badge status changed from 'No' to 'Yes' by crossing the 4.8 review threshold.

### Assumptions

By defending all the assumptions below, we are able to estimate the LATE.

#### Regression Discontinuity (RDD) Assumptions
The only assumption related to the RDD design is that the potential outcomes of having a Superhost badge and not having one are continuous at the 4.8 average review rating cutoff.

A heuristic to understnad this assumption is that near the 4.8 rating cutoff, whether a host gets the Superhost badge or not is up to random chance. This means that hosts close to the cutoff are comparable, since they have similar observed characteristics and unobserved characteristics (host quality, response rate, cancelation rate, etc.). This is often called **local randomization**

#### Additional Assumptions for a Fuzzy RDD
Because we are using a Fuzzy RDD design, we have some additional assumptions that are from the Instrumental Variables Design. These assumptions must hold for a local region around the cutoff:
1. Ignorability of the Instrument - This has 2 parts:
  - Whether someone is slightly above or below the cutoff is as-if randomly assigned. Imagine in scenario A host Joe has a kind reviewer that gives him 5 stars and Joe's average rating is 4.81 (above the threshold). In scenario B, Joe could have a angry reviewer that gives him 0 stars by chance, making his average rating 4.78 (below the threshold). Whether Joe is above or below the cutoff is almost random, as long as Joe is close to the cutoff.
  - Exclusion: The 4.8 threshold can only affect the number of reviews in the last 12 months through the fact that it allows users to get the Superhost badge
2. Relevance - This is saying that the 4.8 threshold affects whether someone receives the Superhost badge or not. This seems reasonable since this threshold is one of many criteria for earning a Superhost badge.
3. Monotonicity - This means there are defiers, which means there are no hosts who would not have a Superhost badge when they cross the 4.8 threshold AND have a badge when they are below the threshold. Having such a host is impossible because a host cannot get a Superhost badge if they are below the rating threshold.

TODO:

### Data Processing
- Load all data into a DuckDB db in load.py
- Get data into correct form using dbt (after planning)

Final form of data
- Feb and Jan 2025 are missing 
- all in duckdb
- raw data will not be on Github

### Setup

1. Clone repo
2. Run download.py, which will create the data/ directory, containing the raw listings
3. Run load.py, which will create a listings.db file in the data/ directory, which is the DuckDB database


