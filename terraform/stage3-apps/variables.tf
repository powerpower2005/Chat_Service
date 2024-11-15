# Frontend/Backend 버전
variable "frontend_version" {
  description = "Frontend application version"
  type        = string
  default     = "latest"
}

variable "backend_version" {
  description = "Backend application version"
  type        = string
  default     = "latest"
}

variable "github_username" {
  description = "GitHub username for container registry"
  type        = string
  default     = "powerpower2005"
}