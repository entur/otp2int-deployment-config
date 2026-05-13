# Contains main description of bulk of terraform?
terraform {
  required_version = "~> 1.14"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.49.0"
    }
  }
}

provider "google" {}

resource "google_storage_bucket_iam_member" "report_entur_reader" {
  bucket = google_storage_bucket.storage_bucket.name
  role   = "roles/storage.objectViewer"
  member = "domain:entur.org"
  condition {
    title      = "report_prefix_only"
    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.storage_bucket.name}/objects/report/')"
  }
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
