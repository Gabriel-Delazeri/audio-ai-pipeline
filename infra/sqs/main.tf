resource "aws_sqs_queue" "audio_dlq" {
  name = var.dlq_name
}

resource "aws_sqs_queue" "audio_processing" {
  name                       = var.queue_name
  visibility_timeout_seconds = 300

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.audio_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })
}