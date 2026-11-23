# ==============================================================================
# Main Terraform Configuration: AWS Infrastructure Provisioning
# Provisions: VPC, Subnet, Security Groups, SSH Key, and 2 EC2 Instances
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# ------------------------------------------------------------------------------
# 1. NETWORKING: VPC, Internet Gateway, Subnet & Route Table
# ------------------------------------------------------------------------------

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone != "" ? var.availability_zone : data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ------------------------------------------------------------------------------
# 2. SECURITY GROUPS: Monitoring Server SG and Application Server SG
# ------------------------------------------------------------------------------

# Security Group for Nagios Monitoring Server
resource "aws_security_group" "monitor_sg" {
  name        = "${var.project_name}-monitor-sg"
  description = "Security group for Nagios Monitoring Server"
  vpc_id      = aws_vpc.main.id

  # SSH access restricted to administrator IP
  ingress {
    description = "SSH from Administrator"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # Nagios Web UI access
  ingress {
    description = "Nagios Web UI HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # Outbound access for package updates and monitoring reach
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-monitor-sg"
  }
}

# Security Group for Application Server (Flask + Nginx)
resource "aws_security_group" "app_sg" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for Application Server (Flask & Nginx)"
  vpc_id      = aws_vpc.main.id

  # SSH access from Administrator
  ingress {
    description = "SSH from Administrator"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # SSH access from Monitoring Server (for Ansible self-healing recovery actions)
  ingress {
    description     = "SSH from Monitoring Server for Ansible Recovery"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.monitor_sg.id]
  }

  # Public HTTP access for the application frontend & reverse proxy
  ingress {
    description = "Public HTTP entry point via Nginx"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # NRPE monitoring checks: restricted STRICTLY to Monitoring Server
  ingress {
    description     = "NRPE Daemon access strictly from Monitoring Server"
    from_port       = 5666
    to_port         = 5666
    protocol        = "tcp"
    security_groups = [aws_security_group.monitor_sg.id]
  }

  # Outbound access for updates
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

# ------------------------------------------------------------------------------
# 3. SSH KEY PAIR & EC2 INSTANCES
# ------------------------------------------------------------------------------

# Dynamic lookup for Ubuntu 22.04 LTS AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# Upload SSH Public Key from project keys/ folder
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file(pathexpand(var.ssh_public_key_path))

  tags = {
    Name = "${var.project_name}-key"
  }
}

# 1. Monitoring Server (Nagios Core 4.x + Ansible Engine)
resource "aws_instance" "monitor_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.monitor_sg.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = var.monitor_disk_size
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "${var.project_name}-monitor-server"
    Role = "monitoring"
  }
}

# 2. Application Server (Nginx + Gunicorn + Flask Backend)
resource "aws_instance" "app_server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  key_name                    = aws_key_pair.deployer.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = var.app_disk_size
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "${var.project_name}-app-server"
    Role = "application"
  }
}
