{{ config(
    materialized='table',
    alias='0_cleaned_deals_' ~ get_van_time()
) }}

{% set project_id = env_var('GCP_PROJECT_ID') %}
{% set dataset = env_var('DLT_DATASET_NAME') %}

WITH deduped_deals AS (
  SELECT 
    *,
    ROW_NUMBER() OVER(PARTITION BY asin ORDER BY starts_at DESC) as rn
  FROM `{{ project_id }}.{{ dataset }}.deals_{{ get_van_time() }}`
  WHERE deal_price__value IS NOT NULL
    AND percent_off IS NOT NULL
)

SELECT
  asin,
  title,
  brand,
  deal_price__value AS deal_price,
  list_price__value AS list_price,
  percent_off,
  deal_type,
  is_lightning_deal,
  deal_badge,
  starts_at,
  ends_at,
  CASE 
    WHEN percent_off > 50 THEN TRUE 
    ELSE FALSE 
  END AS is_high_discount
FROM deduped_deals
WHERE rn = 1