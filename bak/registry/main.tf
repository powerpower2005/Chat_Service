resource "kubernetes_persistent_volume" "registry" {
  metadata {
    name = "registry-pv"
  }

  spec {
    capacity = {
      storage = var.storage_size
    }
    access_modes = ["ReadWriteOnce"]
    storage_class_name = "standard"
    persistent_volume_reclaim_policy = "Retain"
    persistent_volume_source {
      host_path {
        path = var.storage_path
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "registry" {
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
    volume_name = kubernetes_persistent_volume.registry.metadata[0].name
  }
}

resource "kubernetes_deployment" "registry" {
  metadata {
    name      = "registry"
    namespace = var.namespace
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "registry"
      }
    }

    template {
      metadata {
        labels = {
          app = "registry"
        }
      }

      spec {
        container {
          image = "registry:2"
          name  = "registry"

          port {
            container_port = 5000
          }

          volume_mount {
            name       = "registry-storage"
            mount_path = "/var/lib/registry"
          }
        }

        volume {
          name = "registry-storage"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.registry.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "registry" {
  metadata {
    name      = "registry"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = "registry"
    }

    port {
      port        = 5000
      target_port = 5000
    }

    type = "NodePort"
  }
} 