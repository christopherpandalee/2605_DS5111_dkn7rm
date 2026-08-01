{{ config(materialized='table') }}

{% set core_terms = ['python', 'sql', 'dbt', 'snowflake', 'aws', 'docker'] %}

SELECT
    video_id,
    {% for term in core_terms %}
    SUM(CASE WHEN LOWER(tech_term) = '{{ term }}' THEN 1 ELSE 0 END) AS count_{{ term }}_mentions
    {% if not loop.last %},{% endif %}
    {% endfor %}
-- FROM {{ ref('fct_tech_terms') }}  NB:!!!! This notation tells DBT it's a defined model
FROM {{ source('my_database_sources', 'FCT_TECH_TERMS') }}  -- This notation says it pre-exists
GROUP BY video_id
