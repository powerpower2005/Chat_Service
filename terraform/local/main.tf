# 테라폼 상태 관리를 위한 백엔드 설정
# local 로 테라폼의 상태를 관리하는 것은 로컬 환경에서만 하는 것으로
# 협업 시에는 따로 관리할 것
terraform {
  backend "local" {
    path = "terraform.tfstate"  # 로컬 상태 파일 경로
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
