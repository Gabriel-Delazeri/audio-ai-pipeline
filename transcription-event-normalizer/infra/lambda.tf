resource "aws_lambda_function" "normalizer" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_role.arn
  runtime          = var.runtime
  handler          = var.handler
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      TRANSCRIPTION_QUEUE_URL = data.aws_sqs_queue.transcription.url
    }
  }
}

resource "aws_lambda_event_source_mapping" "raw_events_trigger" {
  event_source_arn = data.aws_sqs_queue.raw_events.arn
  function_name    = aws_lambda_function.normalizer.arn
  batch_size       = 10
  enabled          = true
}