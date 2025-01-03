import json
import os
import openai
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")

        # Log all environment variables (excluding sensitive values)
        logger.info("Environment variables present:")
        for key, value in os.environ.items():
            masked_value = "[MASKED]" if "KEY" in key.upper() else value
            logger.info(f"- {key}: {masked_value}")

        # Parse the request body
        try:
            body = json.loads(event.get('body', '{}'))
            text = body.get('text')
            if not text:
                raise ValueError("Request body must contain 'text' key")
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in request body", exc_info=True)
            raise ValueError("Invalid JSON in request body") from e

        # Validate OpenAI API Key
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            logger.error(
                "OpenAI API key is missing from environment variables")
            raise ValueError(
                "OpenAI API key not found in environment variables")

        openai.api_key = api_key
        logger.info("OpenAI API key validated successfully")

        # Call OpenAI API
        logger.info("Making request to OpenAI API")
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system",
                 "content": "You are a medical assistant tasked with extracting structured SIG codes from unstructured text. For each medication, output a JSON object with these fields: medication, sig_code, dosage, frequency, quantity, refills, purpose (if available)."},
                {"role": "user", "content": text}
            ]
        )

        # Process the response
        raw_response = response['choices'][0]['message']['content']
        logger.info(f"Raw response from OpenAI: {raw_response}")

        # Convert the output to JSON
        try:
            medications = json.loads(raw_response)
            logger.info("Successfully parsed OpenAI response into JSON")
        except json.JSONDecodeError as e:
            logger.error(
                "Error parsing OpenAI response into JSON", exc_info=True)
            raise ValueError(
                "Failed to parse OpenAI response into JSON") from e

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'medications': medications,
                'status': 'success'
            })
        }
    except openai.error.InvalidRequestError as e:
        logger.error(f"OpenAI API Invalid Request Error: {e}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f"OpenAI API Invalid Request Error: {e}",
                'status': 'error'
            })
        }
    except openai.error.AuthenticationError as e:
        logger.error(f"OpenAI API Authentication Error: {e}")
        return {
            'statusCode': 401,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f"OpenAI API Authentication Error: {e}",
                'status': 'error'
            })
        }
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f"OpenAI API Error: {e}",
                'status': 'error'
            })
        }
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }
    except Exception:
        logger.error("Unexpected error occurred", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': "An unexpected error occurred. Please check the logs.",
                'status': 'error'
            })
        }
