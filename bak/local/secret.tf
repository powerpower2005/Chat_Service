# terraform/local/secrets.tf
resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = kubernetes_namespace.chat_dev.metadata[0].name
  }

  data = {
    JWT_SECRET      = base64encode(var.jwt_secret)
    MONGODB_URL     = base64encode(var.mongodb_url)
    REDIS_URL       = base64encode(var.redis_url)
    API_BASE_URL    = base64encode(var.api_base_url)
    WS_BASE_URL     = base64encode(var.ws_base_url)
  }

  type = "Opaque"
}