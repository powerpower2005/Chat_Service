variable "namespace" {
  description = "Kubernetes namespace for registry"
  type        = string
}

variable "storage_size" {
  description = "Storage size for registry"
  type        = string
  default     = "10Gi"
}

variable "storage_path" {
  description = "Host path for registry storage"
  type        = string
  default     = "/data/registry"
} 