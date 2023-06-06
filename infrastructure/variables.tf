variable "base_region" {
  default = "eu-central-1"
}

variable "prefix" {
  description = "A simple prefix for all resources related to teacheat application"
  default     = "teacheat"
}

variable "postgres_db" {
  default = "teacheat"
}

variable "postgres_user" {
  default = "dbuser"
}

variable "postgres_password" {
  default = "s3cr3tpassword"
}

variable "postgres_port" {
  default = "5450"
}