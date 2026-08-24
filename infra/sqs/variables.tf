# -------------------------------------------------------
# transcription-raw-events
# -------------------------------------------------------

variable "transcription_raw_events_queue_name" {
  description = "Nome da fila de eventos crus do S3"
  type        = string
  default     = "transcription-raw-events"
}

variable "transcription_raw_events_dlq_name" {
  description = "Nome da dead-letter queue"
  type        = string
  default     = "transcription-raw-events-dlq"
}

# -------------------------------------------------------
# transcription
# -------------------------------------------------------

variable "transcription_queue_name" {
  description = "Transcriptions queue name"
  type        = string
  default     = "transcription"
}

variable "transcription_dlq_name" {
  description = "Transcriptions dead-letter-queue name"
  type        = string
  default     = "transcription-dlq"
}

# -------------------------------------------------------
# S3 - AUDIOS
# -------------------------------------------------------

variable "bucket_name" {
  description = "Name of the audio bucket"
  type = string
  default = "audio"
}

# -------------------------------------------------------
# GENERAL
# -------------------------------------------------------

variable "max_receive_count" {
  description = "Quantas vezes uma mensagem pode falhar antes de ir pra DLQ"
  type        = number
  default     = 3
}