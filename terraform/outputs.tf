output "monitor_public_ip" {
  description = "Public IP of the Nagios Monitoring Server"
  value       = aws_instance.monitor_server.public_ip
}

output "monitor_private_ip" {
  description = "Private IP of the Nagios Monitoring Server (used for internal VPC communications)"
  value       = aws_instance.monitor_server.private_ip
}

output "app_public_ip" {
  description = "Public IP of the Application Server"
  value       = aws_instance.app_server.public_ip
}

output "app_private_ip" {
  description = "Private IP of the Application Server (monitored by Nagios)"
  value       = aws_instance.app_server.private_ip
}

output "nagios_dashboard_url" {
  description = "Nagios Core Web Interface URL"
  value       = "http://${aws_instance.monitor_server.public_ip}/nagios"
}

output "app_url" {
  description = "Public Application URL (served via Nginx reverse proxy)"
  value       = "http://${aws_instance.app_server.public_ip}/"
}

output "ssh_monitoring_server" {
  description = "SSH command to connect to the Monitoring Server"
  value       = "ssh -i ${var.ssh_private_key_path} ubuntu@${aws_instance.monitor_server.public_ip}"
}

output "ssh_app_server" {
  description = "SSH command to connect to the Application Server"
  value       = "ssh -i ${var.ssh_private_key_path} ubuntu@${aws_instance.app_server.public_ip}"
}

output "ansible_inventory" {
  description = "Generated Ansible inventory content"
  value       = <<-EOT
[monitoring]
monitor-server ansible_host=${aws_instance.monitor_server.public_ip} internal_ip=${aws_instance.monitor_server.private_ip}

[webservers]
app-server ansible_host=${aws_instance.app_server.public_ip} internal_ip=${aws_instance.app_server.private_ip}

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=${var.ssh_private_key_path}
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
app_server_private_ip=${aws_instance.app_server.private_ip}
monitor_server_private_ip=${aws_instance.monitor_server.private_ip}
EOT
}
