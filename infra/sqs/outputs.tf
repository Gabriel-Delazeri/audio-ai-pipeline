output "audio_processing_queue_url" {
  value = aws_sqs_queue.audio_processing.url
}

output "audio_processing_queue_arn" {
  value = aws_sqs_queue.audio_processing.arn
}

output "audio_dlq_url" {
  value = aws_sqs_queue.audio_dlq.url
}

output "audio_dlq_arn" {
  value = aws_sqs_queue.audio_dlq.arn
}