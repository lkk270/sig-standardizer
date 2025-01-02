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

# Reference existing IAM role instead of creating one
data "aws_iam_role" "existing_lambda_role" {
  name = "sig-standardizer-lambda-execution"
}

# Create Lambda layer for Tesseract
resource "aws_lambda_layer_version" "tesseract" {
  filename            = "../tesseract-layer.zip"
  layer_name         = "tesseract"
  description        = "Tesseract OCR binaries and libraries"
  compatible_runtimes = ["python3.9"]
}

# Create Lambda function for text extraction
resource "aws_lambda_function" "extract_text" {
  filename         = "../function.zip"
  function_name    = "extract-text"
  role            = data.aws_iam_role.existing_lambda_role.arn
  handler         = "extract.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 512
  force_destroy   = true

  layers = [aws_lambda_layer_version.tesseract.arn]

  tags = {
    Name        = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
  }
}

# Create Lambda function for text standardization
resource "aws_lambda_function" "standardize_text" {
  filename      = "../standardize_function.zip"
  function_name = "standardize-text"
  role         = data.aws_iam_role.existing_lambda_role.arn
  handler      = "standardize.lambda_handler"
  runtime      = "python3.9"
  timeout      = 60
  memory_size  = 1024
  force_destroy = true

  environment {
    variables = {
      OPENAI_API_KEY = var.openai_api_key
      PYTHONPATH     = "/opt/python"
    }
  }
}

# Create function URLs
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