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

output "efs_csi_sa_role" {
  value = module.efs_csi_irsa_role.iam_role_arn
}

output "efs_id" {
  value = aws_efs_file_system.data.id
}

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = module.db.db_instance_address
}