variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "XXXXXX"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "XXXXXX"
}

variable "job_name" {
  description = "Cloud Run Job Name"
  type        = string
  default     = "XXXXXX"
}

variable "container_image" {
  description = "Container image address"
  type        = string
  default     = "XXXXXX"
}

variable "service_account_email" {
  description = "Service account to run the job"
  type        = string
  default     = "XXXXXX"
}