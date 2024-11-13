terraform {
  required_providers {
    # Kubernetes 프로바이더 설정
    kubernetes = {
      source  = "hashicorp/kubernetes"  # 공식 Hashicorp Kubernetes 프로바이더 사용
      version = "~> 2.0"                # 2.x 버전 사용 (호환성 보장)
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
}

# Kubernetes 프로바이더 구성
provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}