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

        # Parse the request body
        body = json.loads(event['body'])
        text = body['text']

        # Log OpenAI API key presence (not the key itself)
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OpenAI API key not found in environment variables")

        logger.info("Initializing OpenAI client")
        client = openai.OpenAI(api_key=api_key)

        logger.info("Making request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Standardize the following signature block format."},
                {"role": "user", "content": text}
            ]
        )

        standardized_text = response.choices[0].message.content
        logger.info("Successfully received response from OpenAI")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'text': standardized_text,
                'status': 'success'
            })
        }
    except openai.APIError as e:
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
