resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "backend"
    namespace = var.namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "backend"
      }
    }

    template {
      metadata {
        labels = {
          app = "backend"
        }
      }

      spec {
        container {
          name  = "backend"
          image = var.image

          port {
            container_port = 8000
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

resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend"
    namespace = var.namespace
  }

  spec {
    type = var.service_type

    selector = {
      app = "backend"
    }

    port {
      port        = 8000
      target_port = 8000
    }
  }
} 