output "service_name" {
  description = "Name of the registry service"
  value       = kubernetes_service.registry.metadata[0].name
}

output "service_namespace" {
  description = "Namespace of the registry service"
  value       = kubernetes_service.registry.metadata[0].namespace
}

output "service_port" {
  description = "Port of the registry service"
  value       = kubernetes_service.registry.spec[0].port[0].port
} 