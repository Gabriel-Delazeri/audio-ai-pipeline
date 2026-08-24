# -------------------------------------------------------
# SQS / S3 (recursos globais já existentes)
# -------------------------------------------------------

variable "bucket_name" {
  description = "Nome do bucket de áudios"
  type        = string
  default     = "audio"
}

variable "transcription_queue_name" {
  description = "Nome da fila consumida por este serviço"
  type        = string
  default     = "transcription"
}

# -------------------------------------------------------
# RDS - PostgreSQL
# -------------------------------------------------------

variable "db_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "transcriptions"
}

variable "db_username" {
  description = "Usuário do banco"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Senha do banco (uso local/LocalStack apenas)"
  type        = string
  default     = "postgres"
  sensitive   = true
}

variable "db_instance_class" {
  description = "Classe da instância RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "db_port" {
  description = "Porta do PostgreSQL"
  type        = number
  default     = 5432
}

# -------------------------------------------------------
# ECS
# -------------------------------------------------------

variable "cluster_name" {
  description = "Nome do cluster ECS"
  type        = string
  default     = "transcription-cluster"
}

variable "service_name" {
  description = "Nome do serviço ECS"
  type        = string
  default     = "transcription-service"
}

variable "container_image" {
  description = "Imagem Docker do worker (ex: repo-ecr:tag). Deve ser buildada e enviada antes do apply"
  type        = string
  default     = "transcription-service:latest"
}

variable "task_cpu" {
  description = "CPU da task Fargate"
  type        = string
  default     = "1024"
}

variable "task_memory" {
  description = "Memória da task Fargate"
  type        = string
  default     = "3072"
}

variable "desired_count" {
  description = "Quantidade de instâncias do worker"
  type        = number
  default     = 1
}

variable "whisper_model" {
  description = "Modelo do Whisper a ser carregado"
  type        = string
  default     = "base"
}
