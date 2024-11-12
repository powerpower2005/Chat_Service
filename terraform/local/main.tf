# terraform/local/main.tf
resource "kubernetes_namespace" "chat_dev" {
  metadata {
    name = "chat-dev"
    labels = {
      environment = "development"
    }
  }
}

# MongoDB 설정
module "mongodb" {
  source = "../modules/mongodb"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
}

# Redis 설정
module "redis" {
  source = "../modules/redis"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
}

# ArgoCD 설정
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = "argocd"
  
  set {
    name  = "server.service.type"
    value = "NodePort"
  }
}