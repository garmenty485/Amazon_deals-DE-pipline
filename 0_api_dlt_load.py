import dlt
import requests
from dotenv import load_dotenv
import os
from extract_brands import extract_brand
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()

# Get configuration from environment variables
API_KEY = os.getenv("RAINFOREST_API_KEY")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BIGQUERY_LOCATION = os.getenv("DLT_DESTINATION_BIGQUERY_LOCATION")
PIPELINE_NAME = os.getenv("DLT_PIPELINE_NAME")
DATASET_NAME = os.getenv("DLT_DATASET_NAME")  # Same as Terraform dataset_id
AMAZON_DOMAIN = os.getenv("AMAZON_DOMAIN")
TIMEZONE = os.getenv("TIMEZONE")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCP_CREDENTIALS_PATH")

# Rainforest API data source function
def fetch_rainforest_deals(api_key, amazon_domain):
    url = "https://api.rainforestapi.com/request"
    params = {
        "api_key": api_key,
        "type": "deals",
        "amazon_domain": amazon_domain
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        deals = data.get("deals_results", [])
        for deal in deals:
            deal["brand"] = extract_brand(deal.get("title", ""))
        return deals
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

# Get current time in the specified timezone
tz = pytz.timezone(TIMEZONE)
current_datetime = datetime.now(tz)
current_date = current_datetime.strftime("%Y%m%d%H")  # e.g. "2025041415"
table_name = f"deals_{current_date}"

# Set up BigQuery pipeline
pipeline = dlt.pipeline(
    pipeline_name=PIPELINE_NAME,
    destination="bigquery",
    dataset_name=DATASET_NAME
)

# Use dynamic table name
@dlt.resource(
    name=table_name,
    write_disposition="replace",
    primary_key=["asin"],
    table_name=table_name,
    columns={
        "deal_price__value": {"data_type": "double", "nullable": True},
        "list_price__value": {"data_type": "double", "nullable": True},
        "current_price__value": {"data_type": "double", "nullable": True}
    }
)
def get_deals():
    for deal in fetch_rainforest_deals(api_key=API_KEY, amazon_domain=AMAZON_DOMAIN):
        deal_price = deal.get("deal_price", {})
        list_price = deal.get("list_price", {})
        current_price = deal.get("current_price", {})

        yield {
            "asin": deal.get("asin"),
            "title": deal.get("title"),
            "brand": deal.get("brand"),
            "deal_price__value": deal_price.get("value"),
            "deal_price__currency": deal_price.get("currency"),
            "deal_price__symbol": deal_price.get("symbol"),
            "current_price__value": current_price.get("value"),
            "current_price__currency": current_price.get("currency"),
            "current_price__symbol": current_price.get("symbol"),
            "list_price__value": list_price.get("value"),
            "list_price__currency": list_price.get("currency"),
            "list_price__symbol": list_price.get("symbol"),
            "percent_off": deal.get("percent_off"),
            "deal_type": deal.get("deal_type"),
            "is_lightning_deal": deal.get("is_lightning_deal", False),
            "deal_badge": deal.get("deal_badge"),
            "starts_at": deal.get("starts_at"),
            "ends_at": deal.get("ends_at")
        }

# Run pipeline
info = pipeline.run(get_deals())
print(info)