WITH listings_filtered_cols AS
(
  SELECT -- MAIN VARIABLES
         id AS listing_id,
         host_is_superhost AS has_superhost,
         number_of_reviews_ltm AS num_reviews_l12m,
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
        ( 1.0 *
          SUM(listing_rating * num_listing_reviews) OVER (PARTITION BY host_id) /
          SUM(num_listing_reviews) OVER (PARTITION BY host_id)
        )  AS host_overall_rating,
        has_superhost,
        num_reviews_l12m,
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
)

SELECT listing_id,
       host_id,
       host_overall_rating
FROM listings_aggregated_stats
LIMIT 5;
