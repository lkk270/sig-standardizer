terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Create an IAM role for the Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "sig-standardizer-lambda-execution"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-lambda-execution"
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
  }
}

# Add CloudWatch logging permissions
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# First Lambda (existing extract-text)
resource "aws_lambda_function" "extract_text" {
  filename         = "../function.zip"
  function_name    = "extract-text"
  role            = aws_iam_role.lambda_role.arn
  handler         = "extract.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 512
  
  source_code_hash = filebase64sha256("../function.zip")

  environment {
    variables = {
      PYTHONPATH = "/opt/python"
      STANDARDIZE_FUNCTION_URL = aws_lambda_function_url.standardize_text_url.function_url
    }
  }

  tags = {
    Name        = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
  }
}

# Second Lambda for standardization
resource "aws_lambda_function" "standardize_text" {
  filename         = "../standardize_function.zip"
  function_name    = "standardize-text"
  role            = aws_iam_role.lambda_role.arn
  handler         = "standardize.lambda_handler"
  runtime         = "python3.9"
  timeout         = 60  # Longer timeout for LLM
  memory_size     = 1024
  
  environment {
    variables = {
      PYTHONPATH = "/opt/python"
      OPENAI_API_KEY = var.openai_api_key
    }
  }
}

# Create CloudWatch Log Group with retention
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/extract-text"
  retention_in_days = 14

  tags = {
    Name        = "${var.project_name}-logs"
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
  }
}

# Lambda function URL
resource "aws_lambda_function_url" "extract_text_url" {
  function_name      = aws_lambda_function.extract_text.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = var.allowed_origins
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age          = 86400
  }
}

# Lambda function URL for standardize text
resource "aws_lambda_function_url" "standardize_text_url" {
  function_name      = aws_lambda_function.standardize_text.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = var.allowed_origins
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age          = 86400
  }
} 