resource "aws_ecs_cluster" "transcription" {
  name = var.cluster_name
}

resource "aws_cloudwatch_log_group" "transcription" {
  name              = "/ecs/${var.service_name}"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "transcription" {
  family                   = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory

  execution_role_arn = aws_iam_role.ecs_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = var.service_name
      image     = var.container_image
      essential = true

      environment = [
        { name = "TRANSCRIPTION_QUEUE_URL", value = data.aws_sqs_queue.transcription.url },
        { name = "WHISPER_MODEL", value = var.whisper_model },
        { name = "DB_HOST", value = aws_db_instance.transcriptions.address },
        { name = "DB_PORT", value = tostring(var.db_port) },
        { name = "DB_NAME", value = var.db_name },
        { name = "DB_USER", value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password },
        { name = "AWS_ENDPOINT_URL", value = "http://localstack:4566" },
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.transcription.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "transcription" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.transcription.id
  task_definition = aws_ecs_task_definition.transcription.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = data.aws_subnets.default.ids
    security_groups = [aws_security_group.ecs_task.id]
  }
}
