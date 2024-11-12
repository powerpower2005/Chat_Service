# terraform/local/secrets.tf
resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = kubernetes_namespace.chat_dev.metadata[0].name
  }

  data = {
    JWT_SECRET      = var.jwt_secret
    MONGODB_URL     = var.mongodb_url
    REDIS_URL       = var.redis_url
    API_BASE_URL    = var.api_base_url
    WS_BASE_URL     = var.ws_base_url
  }
}