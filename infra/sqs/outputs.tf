# -------------------------------------------------------
# transcription-raw-events
# -------------------------------------------------------

output "raw_events_queue_url" {
  value = aws_sqs_queue.raw_events.url
}

output "raw_events_queue_arn" {
  value = aws_sqs_queue.raw_events.arn
}

output "raw_events_dlq_url" {
  value = aws_sqs_queue.raw_events_dlq.url
}

output "raw_events_dlq_arn" {
  value = aws_sqs_queue.raw_events_dlq.arn
}

# -------------------------------------------------------
# transcription
# -------------------------------------------------------

output "transcription_queue_url" {
  value = aws_sqs_queue.transcription.url
}

output "transcription_queue_arn" {
  value = aws_sqs_queue.transcription.arn
}

output "transcription_dlq_url" {
  value = aws_sqs_queue.transcription_dlq.url
}

output "transcription_dlq_arn" {
  value = aws_sqs_queue.transcription_dlq.arn
}