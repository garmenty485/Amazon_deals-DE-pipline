project_id = "ABC-123"  # Replace with your GCP project ID

job_name = "ABC-job" # Name it

# Region
region = "us-central1"

# Container image, build and upload your image first
# Format: us-central1-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY]/[IMAGE]:[TAG]
container_image = "us-central1-docker.pkg.dev/ABC-123/ABC-pipelines/ABC-pipeline:latest"

# Service account, must have proper permissions
service_account_email = "example@ABC-123.iam.gserviceaccount.com" # Fill in yourself
