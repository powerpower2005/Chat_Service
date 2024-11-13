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

# Secret 관련 변수들
variable "jwt_secret" {
  description = "Secret key for JWT"
  type        = string
  sensitive   = true
}

variable "mongodb_url" {
  description = "MongoDB connection URL"
  type        = string
  default     = "mongodb://mongodb:27017"
}

variable "redis_url" {
  description = "Redis connection URL"
  type        = string
  default     = "redis://redis:6379"
}

variable "api_base_url" {
  description = "Base URL for API"
  type        = string
  default     = "http://backend:8000"
}

variable "ws_base_url" {
  description = "Base URL for WebSocket"
  type        = string
  default     = "ws://backend:8000"
} 