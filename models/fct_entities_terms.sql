-- Step 3a: Flatten Tech Terms into Fact Table
{{ config(materialized='table') }}
SELECT
    VIDEO_ID,
    f.value::STRING AS TECH_TERM,
    loaded_at AS PROCESSED_AT
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => TECH_TERMS_ARRAY) f


