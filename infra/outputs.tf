output "audio_bucket_name" {
  value = aws_s3_bucket.audio.bucket
}

output "audio_bucket_arn" {
  value = aws_s3_bucket.audio.arn
}