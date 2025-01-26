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
    region      = "europe-southwest1-a"
}