# 필요한 프로바이더 정의
terraform {
  required_providers {
    # Kubernetes 프로바이더 설정
    kubernetes = {
      source  = "hashicorp/kubernetes"  # 공식 Hashicorp Kubernetes 프로바이더 사용
      version = "~> 2.0"                # 2.x 버전 사용 (호환성 보장)
    }
    
    # Helm 프로바이더 설정 
    helm = {
      source  = "hashicorp/helm"        # 공식 Hashicorp Helm 프로바이더 사용
      version = "~> 2.0"                # 2.x 버전 사용 (호환성 보장)
    }
  }
}

# Kubernetes 프로바이더 구성
provider "kubernetes" {
  config_path = "~/.kube/config"        # 로컬 kubeconfig 파일 위치 지정
}

# Helm 프로바이더 구성
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"      # Helm도 동일한 kubeconfig 사용
  }
}