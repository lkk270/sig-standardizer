terraform {
  backend "s3" {
    bucket         = "sig-standardizer-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
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

  # Force update when zip changes
  source_code_hash = filebase64sha256("../tesseract-layer.zip")
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
  
  # Force update when code changes
  source_code_hash = filebase64sha256("../function.zip")

  layers = [
    aws_lambda_layer_version.tesseract.arn
  ]

  tags = {
    Name        = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
  }

  environment {
    variables = {
      TESSDATA_PREFIX = "/opt/lib/tessdata"
      LD_LIBRARY_PATH = "/opt/lib"
    }
  }
}

# Create Lambda function for text standardization
resource "aws_lambda_function" "standardize_text" {
  filename      = "../function.zip"
  function_name = "standardize-text"
  role         = data.aws_iam_role.existing_lambda_role.arn
  handler      = "standardize.lambda_handler"
  runtime      = "python3.9"
  timeout      = 60
  memory_size  = 1024
  
  # Force update when code changes
  source_code_hash = filebase64sha256("../function.zip")

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

import {
  to = aws_lambda_function.extract_text
  id = "extract-text"
}

import {
  to = aws_lambda_function.standardize_text
  id = "standardize-text"
}

import {
  to = aws_lambda_function_url.extract_text_url
  id = "extract-text"
}

import {
  to = aws_lambda_function_url.standardize_text_url
  id = "standardize-text"
} 