resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "frontend"
    namespace = var.namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "frontend"
      }
    }

    template {
      metadata {
        labels = {
          app = "frontend"
        }
      }

      spec {
        container {
          name  = "frontend"
          image = var.image

          port {
            container_port = 3000
          }

          env_from {
            secret_ref {
              name = "app-secrets"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "frontend" {
  metadata {
    name      = "frontend"
    namespace = var.namespace
  }

  spec {
    type = var.service_type

    selector = {
      app = "frontend"
    }

    port {
      port        = 3000
      target_port = 3000
    }
  }
} 