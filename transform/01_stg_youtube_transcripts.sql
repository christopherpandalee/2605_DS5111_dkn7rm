-- Step 1: Staging View (JSON Variant Parsing)
CREATE OR REPLACE TABLE STG_YOUTUBE_TRANSCRIPTS AS
SELECT
    data:video_id::STRING AS VIDEO_ID,
    data:cleaned_text::STRING AS CLEANED_TEXT,
    data:tech_terms AS TECH_TERMS_ARRAY,
    data:book_names AS BOOK_NAMES_ARRAY,
    loaded_at
FROM DKN7RM.RAW_TRANSCRIPTS;
