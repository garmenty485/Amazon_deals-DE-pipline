{{ config(
    materialized='table',
    alias='2_daily_summary_' ~ get_van_time()
) }}

{% set project_id = env_var('GCP_PROJECT_ID') %}
{% set dataset = env_var('DLT_DATASET_NAME') %}

WITH daily_stats AS (
  SELECT 
    DATE(starts_at) as deal_date,
    deal_type,
    COUNT(*) as deal_count,
    AVG(percent_off) as avg_discount,
    COUNT(CASE WHEN is_lightning_deal THEN 1 END) as lightning_deal_count
  FROM `{{ project_id }}.{{ dataset }}.0_cleaned_deals_{{ get_van_time() }}`
  GROUP BY deal_date, deal_type
)

SELECT
  deal_date,
  deal_type,
  deal_count,
  ROUND(avg_discount, 2) as avg_discount_percentage
FROM daily_stats
ORDER BY deal_date DESC, deal_count DESC