## Airbnb Superhost Analysis Overview

Have you thought about being an Airbnb host? While booking properties, you might have seen a cool title for experienced, excellent hosts called "Superhost". To get this title, you have to meet several criteria, and this analysis attempts to quantify the value of having this title for your business.

## Identification Strategy 

The main question is "What is the effect of having Superhost status on bookings for the host's listings?"

## How to become a Superhost

Technically, there are 4 evaluation periods throughout the quarter where qualifying hosts can become superhosts. These four criteria are computed using the host's data from the past 365 days:  
1. Host at least 10 reservations OR 3 reservations that total at least 100 nights over three stays.  
2. Cancelation rate < 10%  
3. >= 90% response rate  
4. >= 4.8 overall rating  

### Setup

1. Clone repo
2. Run download.py, which will create the data/ directory, containing the raw listings
3. Run load.py, which will create a listings.db file in the data/ directory, which is the DuckDB database

---

## dbt Pipeline

```
[Source]
listings (raw CSV — multiple scrape months)
    │
    ▼
[Staging]
listings_filtered_cols (view)
    Selects and renames columns; parses host_response_rate from "95%" → 95.0
    │
    ▼
[Intermediate]
listings_deduped (view)
    Deduplicates to one row per listing_id, keeping the most recent scrape_date
    │
    ▼
[Intermediate]
listings_aggregated_stats (view)
    Computes avg_host_review_score as a review-count-weighted average across
    all of a host's listings (window function over host_id)
    │
    ▼
[Mart]
listings_fuzzy_rdd (table)
    Collapses to one row per host_id. Sums num_reviews_l12m across listings
    as the bookings proxy. Adds binary treatment/qualification indicators
    for use in the RDD.
```

| Model | Layer | Grain | Purpose |
|---|---|---|---|
| `listings_filtered_cols` | Staging | listing × scrape month | Column selection and type casting |
| `listings_deduped` | Intermediate | listing (latest scrape) | Remove duplicate rows across panel months |
| `listings_aggregated_stats` | Intermediate | listing (latest scrape) | Host-level weighted average review score |
| `listings_fuzzy_rdd` | Mart | host | Final analysis dataset for the RDD |
