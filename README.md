# Amazon Deals DE Pipeline

## 1. What does this project do?

This project is an automated data pipeline that fetches Amazon deals data from the Rainforest API, performs data cleaning and statistical analysis, and stores the results in Google BigQuery. It further utilizes dbt for advanced data modeling and reporting. The entire workflow can be deployed on GCP (Google Cloud Platform) and supports automated scheduling.

It generates a original data table, a basic statistic table and 3 fact tables in your bigquery dataset at 9 am everyday. 

![Untitled Diagram drawio](https://github.com/user-attachments/assets/419d7c76-9099-4395-a2e7-eed305b53779)

---

## 2. What can you learn from this project?

- How to connect to third-party APIs and automate data extraction
- Building ETL pipelines with dlt and integrating with BigQuery
- Using PySpark for data processing and statistical analysis
- Data modeling, cleaning, and automated testing with dbt
- Integrating and automating GCP services: BigQuery, Cloud Run, Cloud Scheduler, GCS (with Terraform basics)
- Dockerizing a data pipeline project

Tools included: dlt, pyspark, dbt, BigQuery, Cloud Run, Cloud Scheduler, Terraform

---

## 3. Prerequisites & Setup

1. **GCP Key and Project Setup**
   - Create a GCP project and enable BigQuery, Cloud Run, Cloud Storage, etc.
   - Create a Service Account, download the key file (rename it as `gcp-key.json`), and place it in the project root and deals_dbt/
   - Register https://app.rainforestapi.com/login and get a api key
   - .env is in both root and deals_dbt/, make sure you set both of them (set one of them and just copy it for the other)
   - In both `terraform-bigquery/` and `terraform-cloud-run/`, you need to set terraform.tfvars and variables.tf that should be consistent with .env
   - Create a GCP artifact registry repository (I didn't set it in terraform, you should do it manually)

2. **.env File Setup**
   - Create a `.env` file in the project root. Example:
     ```
     RAINFOREST_API_KEY=your_rainforest_api_key
     GCP_PROJECT_ID=your_gcp_project_id
     DLT_DESTINATION_BIGQUERY_LOCATION=US
     DLT_PIPELINE_NAME=deals_pipeline
     DLT_DATASET_NAME=deals_dataset
     AMAZON_DOMAIN=amazon.de
     TIMEZONE=Europe/Berlin
     GCP_CREDENTIALS_PATH=./gcp-key.json
     TEMP_GCS_BUCKET=your_gcs_temp_bucket
     SPARK_JARS=./spark-3.5-bigquery-0.42.1.jar,./gcs-connector-hadoop3-latest.jar
     HADOOP_HOME=(set this if running on Windows)
     ```
3. **Install Dependencies**
   - `pip install -r requirements.txt`
   - Java is required for PySpark

4. **Try it locally**
   - Run `project_run.py` to see if it has no error

5. **Terraform Deployment**
   - In `terraform-bigquery/`, run `terraform init` and `terraform apply` to build bigquery and temporary bucket (temporary bucket is for pyspark)
   - `docker build -t us-central1-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY]/[IMAGE]:[TAG] .` (this example is for us-central1, change it for yourself)
   - `docker push us-central1-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY]/[IMAGE]:[TAG]` (connect it to GCP cli first)
   - In `terraform-cloud-runy/`, run `terraform init` and `terraform apply` to build a cloud-run job instance and a scheduler

3. **Try it in GCP Cloud-run-jobs**
   - Run the job you just set and see if it has no error
   - Check if the scheduler trigger the job when the time you set (default is 9 am)

---

## 4. Noteworthy Parts

- `0_api_dlt_load.py`:  
  - dlt pipeline design, dynamic table naming, API data extraction, and schema definition
  - Brand name extraction logic (`extract_brands.py`)

- `1_spark_process.py`:  
  - PySpark integration with BigQuery
  - Batch calculation and writing of multiple statistics
  - Dynamic table naming and timezone handling

- `deals_dbt/`:
  - It generates fact tables 
  - dbt project structure, data cleaning (deduplication, field transformation), brand and daily statistics models
  - `schema.yml`: column tests for data quality control
  - `run_dbt.py`: automated dbt clean/run/test

- `terraform-bigquery/`, `terraform-cloud-run/`:  
  - Automated deployment scripts for GCP BigQuery, GCS, Cloud Run, and Cloud Scheduler

- `dockerfile`:  
  - How to integrate ETL pipeline, Spark, dbt, and GCP in a single container

---

## 5. Final Output

it will be like this in Bigquery:
![擷取](https://github.com/user-attachments/assets/e0087607-6b2a-4e85-b833-8e170791a1a1)


---

For more details, please refer to the comments and documentation within each folder and script.
