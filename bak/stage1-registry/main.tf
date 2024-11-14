terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

resource "kubernetes_namespace" "registry" {
  metadata {
    name = "registry"
  }
}

module "registry" {
  source = "../modules/registry"
  
  namespace    = kubernetes_namespace.registry.metadata[0].name
  storage_size = "10Gi"
  storage_path = "/data/registry"
} 