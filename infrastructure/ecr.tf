resource "aws_ecr_repository" "teacheat" {
  name                 = "${var.prefix}-app"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "proxy" {
  name                 = "${var.prefix}-proxy"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_iam_policy" "allow_ecr_teacheat_app" {
  name = "${local.cluster_name}-allow_ecr_teacheat_app"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetAuthorizationToken"
        ],
        Resource = aws_ecr_repository.teacheat.arn
      }
    ]
  })
}

resource "aws_iam_policy" "allow_ecr_teacheat_proxy" {
  name = "${local.cluster_name}-allow_ecr_teacheat_proxy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetAuthorizationToken"
        ],
        Resource = aws_ecr_repository.proxy.arn
      }
    ]
  })
}

