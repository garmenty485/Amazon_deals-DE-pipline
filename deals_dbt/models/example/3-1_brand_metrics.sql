{{ config(
    materialized='table',
    alias='1_brand_metrics_' ~ get_van_time()
) }}

{% set project_id = env_var('GCP_PROJECT_ID') %}
{% set dataset = env_var('DLT_DATASET_NAME') %}

WITH brand_stats AS (
  SELECT 
    brand,
    COUNT(*) as total_deals,
    AVG(percent_off) as avg_discount,
    AVG(deal_price) as avg_deal_price,
    COUNT(CASE WHEN is_high_discount THEN 1 END) as high_discount_deals
  FROM `{{ project_id }}.{{ dataset }}.0_cleaned_deals_{{ get_van_time() }}`
  WHERE brand IS NOT NULL
  GROUP BY brand
)

SELECT
  brand,
  total_deals,
  ROUND(avg_discount, 2) as avg_discount_percentage,
  ROUND(avg_deal_price, 2) as avg_deal_price,
  high_discount_deals,
  ROUND(high_discount_deals / total_deals * 100, 2) as high_discount_percentage
FROM brand_stats
ORDER BY total_deals DESC