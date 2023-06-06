# DOCS: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest


#resource "aws_eip" "nat" {
#  count = 3
#
#  vpc = true
#}


module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 4.0.1"

  name = "${var.prefix}-vpc"
  cidr = "10.0.0.0/16"
  azs = slice(data.aws_availability_zones.zones.names, 0, 3)

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway = true
  single_nat_gateway= true
  enable_dns_hostnames = true
  create_database_subnet_group = true
#  reuse_nat_ips       = true                    # <= Skip creation of EIPs for the NAT Gateways
#  external_nat_ip_ids = "${aws_eip.nat.*.id}"   # <= IPs specified here as input to the module

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.prefix}-cluster" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }


  private_subnet_tags = {
    "kubernetes.io/cluster/${var.prefix}-cluster" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }
}