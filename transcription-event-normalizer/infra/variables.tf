variable "function_name" {
  description = "Nome da Lambda"
  type        = string
  default     = "transcription-event-normalizer"
}

variable "runtime" {
  description = "Runtime Python"
  type        = string
  default     = "python3.12"
}

variable "handler" {
  description = "Arquivo e função de entrada"
  type        = string
  default     = "handler.handler"
}

variable "raw_events_queue_name" {
  description = "Nome da fila de entrada (trigger da Lambda)"
  type        = string
  default     = "transcription-raw-events"
}

variable "transcription_queue_name" {
  description = "Nome da fila destino onde a Lambda publica"
  type        = string
  default     = "transcription"
}