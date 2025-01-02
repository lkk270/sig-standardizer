variable "openai_api_key" {
  description = "OpenAI API key for the standardization Lambda"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment (prod, dev, etc.)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "sig-standardizer"
}

variable "allowed_origins" {
  description = "List of allowed origins for CORS"
  type        = list(string)
  default     = ["http://localhost:3000", "https://your-production-domain.com"]
}
