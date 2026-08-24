data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../app/src"
  output_path = "${path.module}/lambda.zip"
}

data "aws_sqs_queue" "raw_events" {
  name = var.raw_events_queue_name
}

data "aws_sqs_queue" "transcription" {
  name = var.transcription_queue_name
}