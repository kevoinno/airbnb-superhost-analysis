WITH listings_fuzzy_rdd AS (
  SELECT listing_id,
        avg_host_review_score,
        CASE WHEN avg_host_review_score >= 4.8 THEN 1 ELSE 0 END AS qualified_by_avg_host_review_score,
        CASE WHEN has_superhost THEN 1 ELSE 0 END AS has_superhost,
        num_reviews_l12m,
        scrape_date,
        -- COVARIATES
        host_id,
        CASE WHEN host_identity_verified THEN 1 ELSE 0 END AS host_identity_verified,
        neighbourhood_cleansed,
        property_type,
        room_type,
        accommodates,
        bathrooms,
        bedrooms,
        instant_bookable,
        host_since
  FROM {{ ref("listings_aggregated_stats") }}
)

SELECT * FROM listings_fuzzy_rdd
