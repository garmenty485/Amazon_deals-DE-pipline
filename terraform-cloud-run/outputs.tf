# Outputs for terraform-cloud-run
output "cloud_run_job_uri" {
  description = "URI of the Cloud Run Job"
  value       = google_cloud_run_v2_job.test0_pipeline.id # Using id instead of uri
}

output "cloud_run_job_name" {
  description = "Name of the Cloud Run Job"
  value       = google_cloud_run_v2_job.test0_pipeline.name
}

output "scheduler_job_name" {
  description = "Name of the Cloud Scheduler Job"
  value       = google_cloud_scheduler_job.test0_pipeline_scheduler.name
}