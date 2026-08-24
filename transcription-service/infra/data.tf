data "aws_s3_bucket" "audio" {
  bucket = var.bucket_name
}

data "aws_sqs_queue" "transcription" {
  name = var.transcription_queue_name
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
