variable "aws_region" {
  description = "The AWS region to deploy infrastructure into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for all provisioned resources"
  type        = string
  default     = "devops-self-healing"
}

variable "environment" {
  description = "Environment identifier (e.g. dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the dedicated VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the subnet (leave blank for automatic selection)"
  type        = string
  default     = ""
}

variable "admin_ip" {
  description = "Administrator IP or CIDR block authorized for SSH and Nagios Web UI access (e.g., 203.0.113.50/32)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "instance_type" {
  description = "EC2 instance type for both servers (t2.micro / t3.micro are Free Tier eligible)"
  type        = string
  default     = "t2.micro"
}

variable "ssh_public_key_path" {
  description = "Local path to the SSH public key for EC2 instance access"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_private_key_path" {
  description = "Local path to the SSH private key used by Ansible to connect"
  type        = string
  default     = "~/.ssh/id_rsa"
}

variable "monitor_disk_size" {
  description = "Root EBS volume size in GB for the Monitoring Server"
  type        = number
  default     = 20
}

variable "app_disk_size" {
  description = "Root EBS volume size in GB for the Application Server"
  type        = number
  default     = 10
}
