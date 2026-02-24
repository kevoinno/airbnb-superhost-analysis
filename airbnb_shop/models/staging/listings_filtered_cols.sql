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
  FROM {{ ref("listings") }}
)

SELECT * FROM listings_filtered_cols
