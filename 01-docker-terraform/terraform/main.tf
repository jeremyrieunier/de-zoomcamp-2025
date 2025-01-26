terraform {
    required_providers {
        google = {
        source = "hashicorp/google"
        version = "6.17.0"
        }
    }
}

provider "google" {
    project     = "terraform-demo-448914"
    region      = "europe-southwest"
}

resource "google_storage_bucket" "demo-bucket" {
    name          = "terraform-demo-448914-terra-bucket"
    location      = "EU"
    force_destroy = true

    lifecycle_rule {
        condition {
            age = 1
        }
        action {
            type = "AbortIncompleteMultipartUpload"
        }
    }
}