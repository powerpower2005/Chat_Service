resource "kubernetes_persistent_volume" "registry_pv" {
  metadata {
    name = "registry-pv"
  }
  spec {
    capacity = {
      storage = var.storage_size
    }
    access_modes = ["ReadWriteOnce"]
    storage_class_name = "standard"
    persistent_volume_source {
      host_path {
        path = var.storage_path
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "registry_pvc" {
  metadata {
    name      = "registry-pvc"
    namespace = var.namespace
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = var.storage_size
      }
    }
    storage_class_name = "standard"
  }
}

resource "kubernetes_deployment" "registry" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.name
      }
    }

    template {
      metadata {
        labels = {
          app = var.name
        }
      }

      spec {
        container {
          image = var.registry_image
          name  = var.name

          port {
            container_port = var.container_port
          }

          volume_mount {
            name       = "registry-storage"
            mount_path = "/var/lib/registry"
          }
        }

        volume {
          name = "registry-storage"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.registry_pvc.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "registry" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = var.name
    }

    port {
      port        = var.service_port
      target_port = var.container_port
    }

    type = var.service_type
  }
} 