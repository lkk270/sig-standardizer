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
        for key in os.environ:
            logger.info(
                f"- {key}: {'[MASKED]' if 'KEY' in key.upper() else os.environ[key]}")

        # Parse the request body
        body = json.loads(event['body'])
        text = body['text']

        # Validate OpenAI API Key
        api_key = os.environ.get('OPENAI_API_KEY')
        logger.info(f"OpenAI API key present: {api_key is not None}")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found in environment variables")

        # Call OpenAI API
        openai.api_key = api_key
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
                "Error parsing OpenAI response into JSON, specific error: " + str(e), exc_info=True)
            raise ValueError(
                "OpenAI API key not found in environment variables") from None

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
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f"OpenAI API Error: {str(e)}",
                'status': 'error'
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }
