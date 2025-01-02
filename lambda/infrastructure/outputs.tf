output "extract_text_function_name" {
  description = "Name of the text extraction Lambda function"
  value       = aws_lambda_function.extract_text.function_name
}

output "extract_text_function_arn" {
  description = "ARN of the text extraction Lambda function"
  value       = aws_lambda_function.extract_text.arn
}

output "extract_text_url" {
  description = "URL endpoint for the text extraction Lambda"
  value       = aws_lambda_function_url.extract_text_url.function_url
}

output "standardize_text_function_name" {
  description = "Name of the text standardization Lambda function"
  value       = aws_lambda_function.standardize_text.function_name
}

output "standardize_text_function_arn" {
  description = "ARN of the text standardization Lambda function"
  value       = aws_lambda_function.standardize_text.arn
}

output "standardize_text_url" {
  description = "URL endpoint for the text standardization Lambda"
  value       = aws_lambda_function_url.standardize_text_url.function_url
}
