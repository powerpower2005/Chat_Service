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

# ArgoCD 네임스페이스 생성
resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

# ArgoCD Helm 차트 설치
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.7.2"
  namespace  = kubernetes_namespace.argocd.metadata[0].name  # 생성된 네임스페이스 참조

  # ArgoCD 서비스를 NodePort로 설정
  set {
    name  = "server.service.type"
    value = "NodePort"
  }

  # 네임스페이스가 생성된 후에 설치
  depends_on = [kubernetes_namespace.argocd]
}

# 레지스트리를 위한 네임스페이스 생성
resource "kubernetes_namespace" "registry" {
  metadata {
    name = "registry"
  }
}

# 레지스트리 모듈 호출
module "registry" {
  source = "../modules/registry"
  
  namespace    = kubernetes_namespace.registry.metadata[0].name
  storage_size = "10Gi"
  storage_path = "/data/registry"
  
  # 필요한 경우 다른 변수들도 오버라이드 가능
  # name = "custom-registry"
  # service_type = "ClusterIP"
}

# 프론트엔드 모듈
module "frontend" {
  source    = "../modules/frontend"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
  
  image     = "localhost:5000/chat-frontend:${var.frontend_version}"
  replicas  = 1
  
  service_type = "NodePort"  # 로컬 개발환경에서 접근하기 위해
}

# 백엔드 모듈
module "backend" {
  source    = "../modules/backend"
  namespace = kubernetes_namespace.chat_dev.metadata[0].name
  
  image     = "localhost:5000/chat-backend:${var.backend_version}"
  replicas  = 1
  
  service_type = "ClusterIP"
  
  depends_on = [
    module.mongodb,
    module.redis
  ]
}
