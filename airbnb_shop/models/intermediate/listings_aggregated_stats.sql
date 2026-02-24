WITH listings_aggregated_stats AS
(
  SELECT -- MAIN VARIABLES
        listing_id,
        ROUND( 1.0 *
          SUM(listing_rating * num_listing_reviews) OVER (PARTITION BY host_id) /
          SUM(num_listing_reviews) OVER (PARTITION BY host_id)
        , 3)  AS avg_host_review_score,
        has_superhost,
        num_reviews_l12m,
        scrape_date,
        -- COVARIATES
        host_id,
        host_identity_verified,
        neighbourhood_cleansed,
        property_type,
        room_type,
        accommodates,
        bathrooms,
        bedrooms,
        instant_bookable,
        host_since
  FROM {{ ref("listings_filtered_cols") }}
)

SELECT * FROM listings_aggregated_stats
