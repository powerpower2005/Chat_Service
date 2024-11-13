variable "namespace" {
  description = "Kubernetes namespace for the registry"
  type        = string
  default     = "registry"
}

variable "name" {
  description = "Name for the registry deployment and service"
  type        = string
  default     = "registry"
}

variable "storage_size" {
  description = "Storage size for the registry"
  type        = string
  default     = "10Gi"
}

variable "storage_path" {
  description = "Host path for registry storage"
  type        = string
  default     = "/data/registry"
}

variable "registry_image" {
  description = "Docker image for registry"
  type        = string
  default     = "registry:2"
}

variable "replicas" {
  description = "Number of registry replicas"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "Container port for registry"
  type        = number
  default     = 5000
}

variable "service_port" {
  description = "Service port for registry"
  type        = number
  default     = 5000
}

variable "service_type" {
  description = "Service type for registry"
  type        = string
  default     = "NodePort"
} 