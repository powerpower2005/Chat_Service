terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

module "frontend" {
  source    = "../modules/frontend"
  namespace = "chat-dev"
  image     = "ghcr.io/${var.github_username}/chat_service/chat-frontend:${var.frontend_version}"
  replicas  = 1
}

module "backend" {
  source    = "../modules/backend"
  namespace = "chat-dev"
  image     = "ghcr.io/${var.github_username}/chat_service/chat-backend:${var.backend_version}"
  replicas  = 1
}
