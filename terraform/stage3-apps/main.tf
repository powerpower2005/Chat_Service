terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.7.2"
  namespace  = kubernetes_namespace.argocd.metadata[0].name

  set {
    name  = "server.service.type"
    value = "NodePort"
  }
}

module "frontend" {
  source      = "../../modules/frontend"
  namespace   = "chat-dev"
  image       = "localhost:5000/chat-frontend:${var.frontend_version}"
  replicas    = 1
  service_type = "NodePort"
}

module "backend" {
  source      = "../../modules/backend"
  namespace   = "chat-dev"
  image       = "localhost:5000/chat-backend:${var.backend_version}"
  replicas    = 1
  service_type = "ClusterIP"
  
  depends_on = [
    module.mongodb,
    module.redis
  ]
} 