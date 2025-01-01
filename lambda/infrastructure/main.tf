terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"  # or your preferred region
}

# Lambda function
resource "aws_lambda_function" "extract_text" {
  filename         = "../function.zip"
  function_name    = "extract-text"
  role            = aws_iam_role.lambda_role.arn
  handler         = "main.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 512  # Increased for image processing

  environment {
    variables = {
      PYTHONPATH = "/opt/python"
    }
  }
}

# Lambda function URL
resource "aws_lambda_function_url" "extract_text_url" {
  function_name      = aws_lambda_function.extract_text.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["http://localhost:3000", "https://your-production-domain.com"]
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age          = 86400
  }
}

# Output the function URL
output "lambda_url" {
  value = aws_lambda_function_url.extract_text_url.url
} 