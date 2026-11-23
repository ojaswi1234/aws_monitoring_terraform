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

  # Nagios Web UI access restricted to administrator IP
  ingress {
    description = "Nagios Web Dashboard HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.admin_ip]
  }

  # ICMP Ping from admin
  ingress {
    description = "ICMP Ping from Admin"
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = [var.admin_ip]
  }

  # Outbound access for package installation, updates, and monitoring checks
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

resource "aws_security_group" "app_sg" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for Application Server (Nginx, Gunicorn, Flask)"
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

  # ICMP Ping from Monitoring Server
  ingress {
    description     = "ICMP Ping from Monitoring Server"
    from_port       = -1
    to_port         = -1
    protocol        = "icmp"
    security_groups = [aws_security_group.monitor_sg.id]
  }

  # Outbound internet access for system updates & dependencies
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
