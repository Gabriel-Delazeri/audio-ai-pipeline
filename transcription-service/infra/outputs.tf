output "db_endpoint" {
  value = aws_db_instance.transcriptions.address
}

output "db_port" {
  value = aws_db_instance.transcriptions.port
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.transcription.name
}

output "ecs_service_name" {
  value = aws_ecs_service.transcription.name
}
