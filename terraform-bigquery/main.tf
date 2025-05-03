# Set up Terraform provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Configure Google provider
provider "google" {
  project     = var.project_id
  credentials = file(var.credentials_path)
  region      = var.region
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "test_set" {
  dataset_id  = "XXXXXX"
  location    = "XXXXXX"
  description = "XXXXXX"
}

# Create GCS bucket
resource "google_storage_bucket" "test_bucket" {
  name                        = "XXXXXX"
  location                    = "XXXXXX"
  uniform_bucket_level_access = var.gcs_uniform_bucket_level_access
}