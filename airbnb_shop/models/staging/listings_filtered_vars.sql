SELECT id AS listing_id,
       last_scraped,
       review_scores_rating,
       host_is_superhost,
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
FROM {{ ref("listings") }}

