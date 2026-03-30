{{ config(materialized = 'table') }}

SELECT
    host_id,
    ANY_VALUE(avg_host_review_score)                                              AS avg_host_review_score,
    CASE WHEN ANY_VALUE(avg_host_review_score) >= 4.8 THEN 1 ELSE 0 END          AS qualified_by_avg_host_review_score,
    ANY_VALUE(CASE WHEN has_superhost THEN 1 ELSE 0 END)                         AS has_superhost,
    SUM(num_reviews_l12m)                                                         AS num_reviews_l12m,
    MAX(scrape_date)                                                              AS scrape_date,
    -- COVARIATES (host-level attributes — same across all listings for a host)
    ANY_VALUE(CASE WHEN host_identity_verified THEN 1 ELSE 0 END)                AS host_identity_verified,
    ANY_VALUE(host_since)                                                         AS host_since,
    ANY_VALUE(host_response_rate)                                                 AS host_response_rate,
    CASE WHEN ANY_VALUE(host_response_rate) >= 90 THEN 1 ELSE 0 END              AS qualified_by_response_rate,
    AVG(CASE WHEN instant_bookable THEN 1.0 ELSE 0.0 END)                       AS prop_instant_bookable
FROM {{ ref("listings_aggregated_stats") }}
GROUP BY host_id
