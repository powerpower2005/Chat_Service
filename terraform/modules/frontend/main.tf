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
          image_pull_policy = "Always"

          port {
            container_port = 3000
          }

          env_from {
            secret_ref {
              name = "app-secrets"
            }
          }

          resources {
            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }

          env {
            name  = "NGINX_WORKER_PROCESSES"
            value = "1"
          }
          env {
            name  = "NGINX_WORKER_CONNECTIONS"
            value = "1024"
          }
          env {
            name  = "NGINX_WORKER_AIO"
            value = "off"
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
      node_port   = 30000
    }
  }
} 