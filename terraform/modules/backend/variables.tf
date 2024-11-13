variable "namespace" {
  description = "Kubernetes namespace for backend deployment"
  type        = string
}

variable "image" {
  description = "Docker image for backend"
  type        = string
}

variable "replicas" {
  description = "Number of backend replicas"
  type        = number
  default     = 1
}

variable "service_type" {
  description = "Kubernetes service type for backend"
  type        = string
  default     = "ClusterIP"
} 