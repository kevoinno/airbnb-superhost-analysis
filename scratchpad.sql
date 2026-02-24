WITH listings_filtered_cols AS
(
  SELECT -- MAIN VARIABLES
         id AS listing_id,
         host_is_superhost AS has_superhost,
         number_of_reviews_ltm AS num_reviews_l12m,
         last_scraped AS scrape_date,
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
        host_since,
        -- OTHER NEEDED VARIBLES
        review_scores_rating AS listing_rating,
        number_of_reviews AS num_listing_reviews
  FROM raw_listings
),

listings_aggregated_stats AS
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
  FROM listings_filtered_cols
),

listings_fuzzy_rdd AS (
  SELECT listing_id,
        avg_host_review_score,
        CASE WHEN avg_host_review_score > 4.8 THEN 1 ELSE 0 END AS qualified_by_avg_host_review_score,
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
  FROM listings_aggregated_stats
)

SELECT  *
FROM listings_fuzzy_rdd
LIMIT 10
;
