# Contains main description of bulk of terraform?
terraform {
  required_version = ">= 0.13.2"
}

provider "google" {
  version = "~> 4.84.0"
}
# Create bucket
resource "google_storage_bucket" "storage_bucket" {
  name                        = "${var.bucket_instance_prefix}-${var.bucket_instance_suffix}"
  force_destroy               = var.force_destroy
  location                    = var.location
  project                     = var.storage_project
  storage_class               = var.storage_class
  labels                      = var.labels
  uniform_bucket_level_access = true
  versioning {
    enabled = var.versioning
  }
  logging {
    log_bucket        = var.log_bucket
    log_object_prefix = "${var.bucket_instance_prefix}-${var.bucket_instance_suffix}"
  }
}
