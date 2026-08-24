# -------------------------------------------------------
# audio - s3
# -------------------------------------------------------

data "aws_s3_bucket" "audio" {
  bucket = var.bucket_name
}


# -------------------------------------------------------
# transcription-raw-events
# -------------------------------------------------------

resource "aws_sqs_queue" "raw_events_dlq" {
  name = var.transcription_raw_events_dlq_name
}

resource "aws_sqs_queue" "raw_events" {
  name                       = var.transcription_raw_events_queue_name
  visibility_timeout_seconds = 300

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.raw_events_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.raw_events.url

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "s3.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.raw_events.arn
      Condition = {
        ArnLike = {
          "aws:SourceArn" = data.aws_s3_bucket.audio.arn
        }
      }
    }]
  })
}

resource "aws_s3_bucket_notification" "audio_upload" {
  bucket = data.aws_s3_bucket.audio.id

  queue {
    queue_arn = aws_sqs_queue.raw_events.arn
    events    = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_sqs_queue_policy.allow_s3]
}

# -------------------------------------------------------
# transcription
# -------------------------------------------------------

resource "aws_sqs_queue" "transcription_dlq" {
  name = var.transcription_dlq_name
}

resource "aws_sqs_queue" "transcription" {
  name                       = var.transcription_queue_name
  visibility_timeout_seconds = 300

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.transcription_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })
}