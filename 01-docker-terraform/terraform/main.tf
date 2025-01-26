terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "${var.project_id}-${var.environment}-bucket"
  location      = var.location
  storage_class = var.storage_class
  force_destroy = true

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dateset_name
  location   = var.location

  labels = {
    environment = var.environment
    project     = var.project_id
  }
}