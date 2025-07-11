# Configure the Google Cloud Provider
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_dependent_services = true
  disable_on_destroy         = false
}

# Cloud Run service
resource "google_cloud_run_service" "main" {
  name     = var.service_name
  location = var.region
  
  template {
    spec {
      containers {
        image = var.container_image
        
        resources {
          limits = {
            cpu    = var.cpu_limit
            memory = var.memory_limit
          }
        }
        
        env {
          name  = "ENVIRONMENT"
          value = var.environment
        }
        
        env {
          name  = "VERSION"
          value = var.app_version
        }
        
        ports {
          container_port = 8080
        }
      }
      
      container_concurrency = var.container_concurrency
      timeout_seconds      = var.timeout_seconds
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.min_scale
        "autoscaling.knative.dev/maxScale" = var.max_scale
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# IAM policy to allow unauthenticated access
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_service.main.location
  service  = google_cloud_run_service.main.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Build trigger for automated deployments
resource "google_cloudbuild_trigger" "deploy_trigger" {
  name        = "${var.service_name}-deploy-trigger"
  description = "Automated deployment trigger for ${var.service_name}"
  
  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = var.deploy_branch
    }
  }
  
  filename = "cloudbuild.yaml"
  
  depends_on = [google_project_service.required_apis]
}