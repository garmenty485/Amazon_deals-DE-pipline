# GCP Project ID
variable "project_id" {
  description = "The ID of the GCP project to deploy resources into"
  type        = string
  default     = "ABC-123"
}

# GCP Service Account Credentials Path
variable "credentials_path" {
  description = "Path to the GCP service account key JSON file"
  type        = string
  default     = "../gcp-key.json"
}

# GCP Region
variable "region" {
  description = "The GCP region for deploying resources"
  type        = string
  default     = "us-east1"
}

# BigQuery Dataset ID
variable "bigquery_dataset_id" {
  description = "The ID of the BigQuery dataset to create"
  type        = string
  default     = "test_set"
}

# BigQuery Dataset Location
variable "bigquery_location" {
  description = "The location for the BigQuery dataset (e.g., US, EU)"
  type        = string
  default     = "US"
}

# BigQuery Dataset Description
variable "bigquery_dataset_description" {
  description = "Description of the BigQuery dataset"
  type        = string
  default     = "Dataset for Amazon deals data from Rainforest API"
}

# GCS Bucket Name
variable "gcs_bucket_name" {
  description = "The globally unique name of the GCS bucket"
  type        = string
  default     = "ABC-bucket"
}

# GCS Bucket Location
variable "gcs_bucket_location" {
  description = "The location for the GCS bucket (e.g., US, ASIA-EAST1)"
  type        = string
  default     = "US"
}

# GCS Bucket Uniform Access Control
variable "gcs_uniform_bucket_level_access" {
  description = "Enable uniform bucket-level access for the GCS bucket"
  type        = bool
  default     = true
}