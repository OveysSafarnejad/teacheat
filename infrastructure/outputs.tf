output "cluster_name" {
  value = module.eks.cluster_name
}

output "region" {
  value = var.base_region
}

output "ecr_teacheat_app_url" {
  value = aws_ecr_repository.teacheat.repository_url
}


output "ecr_teacheat_proxy_url" {
  value = aws_ecr_repository.proxy.repository_url
}