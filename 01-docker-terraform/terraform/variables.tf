variable "project_id" {
    description = "GCP Project ID"
    type        = string
    default     = "terraform-demo-448914"
}

variable "region" {
    description = "Region for GCP resources"
    type        = string   
    default     = "europe-southwest"
}

variable "location" {
    description = "Location for GCP resources"
    type        = string   
    default     = "EU"
}


variable "storage_class" {
    description = "Storage class for GCS bucket"
    type        = string
    default     = "STANDARD"
}


variable "bq_dateset_name" {
    description = "My BQ data set name"
    default     = "demo_dataset"
}

variable "environment" {
    description = "Environment (dev/prod)"
    default     = "dev"
    type        = string
}