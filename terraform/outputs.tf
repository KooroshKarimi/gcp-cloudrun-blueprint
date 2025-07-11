output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.main.status[0].url
}

output "service_name" {
  description = "The name of the Cloud Run service"
  value       = google_cloud_run_service.main.name
}

output "service_location" {
  description = "The location of the Cloud Run service"
  value       = google_cloud_run_service.main.location
}

output "latest_ready_revision_name" {
  description = "The name of the latest ready revision"
  value       = google_cloud_run_service.main.status[0].latest_ready_revision_name
}

output "service_id" {
  description = "The unique identifier for the service"
  value       = google_cloud_run_service.main.id
}

output "build_trigger_id" {
  description = "The ID of the Cloud Build trigger"
  value       = google_cloudbuild_trigger.deploy_trigger.id
}

output "build_trigger_name" {
  description = "The name of the Cloud Build trigger"
  value       = google_cloudbuild_trigger.deploy_trigger.name
}