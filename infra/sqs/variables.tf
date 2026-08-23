variable "queue_name" {
  description = "Nome da fila principal de processamento de áudio"
  type        = string
  default     = "audio-processing"
}

variable "dlq_name" {
  description = "Nome da dead-letter queue"
  type        = string
  default     = "audio-processing-dlq"
}

variable "max_receive_count" {
  description = "Quantas vezes uma mensagem pode falhar antes de ir pra DLQ"
  type        = number
  default     = 3
}