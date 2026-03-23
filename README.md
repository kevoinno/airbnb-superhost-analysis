## Airbnb Superhost Analysis Overview

Have you thought about being an Airbnb host? While booking properties, you might have seen a cool title for experienced, excellent hosts called "Superhost". To get this title, you have to meet several criteria, and this analysis attempts to quantify the value of having this title for your business.

## Identification Strategy 

The main question is **"What is the effect of having Superhost status on bookings for the host's listings?"**

Our approach will involve a fuzzy regression discontinuity design.

## Notes on Data Cleaning  
- The same listing "A" can occur many times over the year based on the scraping. For the analysis, we will use the most recent version of the listing to avoid inflating the sample size without adding additional information

## How to become a Superhost

Technically, there are 4 evaluation periods throughout the quarter where qualifying hosts can become superhosts. These four criteria are computed using the host's data from the past 365 days:  
1. Host at least 10 reservations OR 3 reservations that total at least 100 nights over three stays.  
2. Cancelation rate < 10%  
3. at least a 90% response rate  
4. at least a 4.8 overall rating  

Only 1 and 4 are in the dataset, and the overall host rating is the only reliably measured metric. Therefore 

### Setup

1. Clone repo
2. Run download.py, which will create the data/ directory, containing the raw listings
3. Run load.py, which will create a listings.db file in the data/ directory, which is the DuckDB database


## dbt Pipeline

```
listings (source)
    └── stg_listings_filtered_cols
            └── int_listings_deduped
                    └── int_listings_aggregated_stats
                                └── mart_listings_fuzzy_rdd
```

| Model | Layer | Grain | Purpose |
|---|---|---|---|
| `listings` | Staging | listing × scrape month | View over raw source CSV data |
| `listings_filtered_cols` | Staging | listing × scrape month | Column selection and type casting (parses `host_response_rate` from "95%" → 95.0) |
| `listings_deduped` | Intermediate | listing (latest scrape) | Deduplicates panel data to one row per listing, keeping most recent scrape |
| `listings_aggregated_stats` | Intermediate | listing (latest scrape) | Adds `avg_host_review_score`: review-count-weighted average across all of a host's listings |
| `listings_fuzzy_rdd` | Mart | **host** | Final RDD dataset — one row per host, `num_reviews_l12m` summed across listings, binary treatment indicators |

To view interactive docs:

```bash
uv run dbt docs generate && uv run dbt docs serve
```
