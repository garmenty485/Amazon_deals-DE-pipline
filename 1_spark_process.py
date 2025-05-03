import os
import platform
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg, count, max, min, col, countDistinct,
    when, round, datediff, current_timestamp,
    sum, desc, lit, first
)
from pyspark.sql.types import FloatType, StringType
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Get HADOOP_HOME from environment variables
os.environ['HADOOP_HOME'] = os.getenv("HADOOP_HOME", "C:\\hadoop")

# Load environment variables
load_dotenv()

# Get configuration from environment variables
GCP_PROJECT_ID = "XXXXXX"
BIGQUERY_DATASET = "XXXXXX"
TEMP_GCS_BUCKET = "XXXXXX"
TIMEZONE = os.getenv("TIMEZONE")
SPARK_JARS = os.getenv("SPARK_JARS", "./spark-3.5-bigquery-0.42.1.jar,./gcs-connector-hadoop3-latest.jar")

# Conditionally set HADOOP_HOME (Windows only)
if platform.system() == "Windows":
    os.environ['HADOOP_HOME'] = os.getenv("HADOOP_HOME", "C:\\hadoop")

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("AmazonCA Deals Processing") \
    .config("spark.jars", SPARK_JARS) \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("spark.hadoop.fs.gs.auth.service.account.enable", "true") \
    .config("spark.hadoop.fs.gs.auth.service.account.json.keyfile", "./gcp-key.json") \
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "./gcp-key.json") \
    .getOrCreate()

spark.conf.set("parentProject", GCP_PROJECT_ID)

# Read data from BigQuery
# Get current time in the specified timezone
tz = pytz.timezone(TIMEZONE)
current_datetime = datetime.now(tz)
current_date = current_datetime.strftime("%Y%m%d%H")  # e.g. "2025041415"

# Format table name, put time at the end
table_name = f"deals_{current_date}"
source_table_name = table_name
stat_table_name = f"deals_stat_{current_date}"

deals_df = spark.read.format("bigquery") \
    .option("table", f"{BIGQUERY_DATASET}.{source_table_name}") \
    .load()

# Find the most common brand
most_common_brand = deals_df.groupBy("brand") \
    .count() \
    .orderBy(desc("count")) \
    .select("brand") \
    .first()[0]

# Calculate all statistics at once
all_stats = deals_df.agg(
    count("*").alias("total_deals"),
    avg("deal_price__value").alias("avg_deal_price"),
    avg("percent_off").alias("avg_discount_percentage"),
    (sum(when(col("is_lightning_deal") == True, 1).otherwise(0)) / count("*") * 100).alias("lightning_deals_percentage"),
    max("deal_price__value").alias("max_deal_price"),
    min("deal_price__value").alias("min_deal_price"),
    max("list_price__value").alias("max_list_price"),
    min("list_price__value").alias("min_list_price"),
    avg(col("list_price__value") - col("deal_price__value")).alias("avg_discount_amount"),
    lit(most_common_brand).alias("most_common_brand")
)

# Write to a single BigQuery table
all_stats.write.format("bigquery") \
    .option("table", f"{BIGQUERY_DATASET}.{stat_table_name}") \
    .option("temporaryGcsBucket", TEMP_GCS_BUCKET) \
    .mode("overwrite") \
    .save()

# Show some key results
all_stats.show()

# Stop SparkSession
spark.stop()