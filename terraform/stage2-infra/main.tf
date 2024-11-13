terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

resource "kubernetes_namespace" "chat_dev" {
  metadata {
    name = "chat-dev"
    labels = {
      environment = "development"
    }
  }
}

module "mongodb" {
  source    = "../../modules/mongodb"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
}

module "redis" {
  source    = "../../modules/redis"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
} 