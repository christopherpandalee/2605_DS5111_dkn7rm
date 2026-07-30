-- Step 3b: Flatten Book Mentions into Fact Table
{{ config(materialized='table') }}
SELECT
    VIDEO_ID,
    f.value::STRING AS BOOK_NAME,
    loaded_at AS PROCESSED_AT
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => BOOK_NAMES_ARRAY) f
