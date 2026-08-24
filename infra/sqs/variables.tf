variable "queue_name" {
  description = "Nome da fila de eventos crus do S3"
  type        = string
  default     = "transcription-raw-events"
}

variable "dlq_name" {
  description = "Nome da dead-letter queue"
  type        = string
  default     = "transcription-raw-events-dlq"
}

variable "max_receive_count" {
  description = "Quantas vezes uma mensagem pode falhar antes de ir pra DLQ"
  type        = number
  default     = 3
}

variable "bucket_name" {
  description = "Name of the audio bucket"
  type = string
  default = "audio"
}