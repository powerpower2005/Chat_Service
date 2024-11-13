output "service_name" {
  description = "Name of the MongoDB service"
  value       = kubernetes_service.mongodb.metadata[0].name
}

output "service_port" {
  description = "Port of the MongoDB service"
  value       = kubernetes_service.mongodb.spec[0].port[0].port
} 