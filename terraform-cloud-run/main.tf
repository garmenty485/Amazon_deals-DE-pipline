provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file("../gcp-key.json")  # XXXXXX
}

# Create Cloud Run Job
resource "google_cloud_run_v2_job" "test0_pipeline" {
  name     = var.job_name
  location = var.region

  deletion_protection = false

  template {
    template {
      containers {
        image = var.container_image
        
        # Optional: configure resource limits
        resources {
          limits = {
            cpu    = "1"
            memory = "2Gi"
          }
        }
      }
      
      # Specify service account
      service_account = var.service_account_email
      
      # Timeout setting
      timeout = "3600s" # 1 hour
    }
  }
}

# Add to main.tf file
# Create Cloud Scheduler Job
resource "google_cloud_scheduler_job" "test0_pipeline_scheduler" {
  name        = "${var.job_name}-scheduler"
  description = "Run Amazon Deals pipeline every day at 9am Vancouver time"
  schedule    = "0 9 * * *"
  time_zone   = "America/Vancouver"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "https://XXXXXX-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/XXXXXX/jobs/XXXXXX:run"
    
    oauth_token {
      service_account_email = var.service_account_email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }
}