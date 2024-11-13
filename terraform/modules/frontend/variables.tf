variable "namespace" {
  description = "Kubernetes namespace for frontend deployment"
  type        = string
}

variable "image" {
  description = "Docker image for frontend"
  type        = string
}

variable "replicas" {
  description = "Number of frontend replicas"
  type        = number
  default     = 1
}

variable "service_type" {
  description = "Kubernetes service type for frontend"
  type        = string
  default     = "NodePort"
} 