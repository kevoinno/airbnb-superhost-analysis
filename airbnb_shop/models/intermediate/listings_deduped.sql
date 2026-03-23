WITH deduped AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY listing_id ORDER BY scrape_date DESC) AS rn
    FROM {{ ref("listings_filtered_cols") }}
)

SELECT * EXCLUDE (rn)
FROM deduped
WHERE rn = 1
