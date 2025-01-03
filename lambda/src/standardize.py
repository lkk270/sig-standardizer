import json
import logging
import os

import openai
from openai import OpenAI

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
                f"- {key}: {'[MASKED]' if 'KEY' in key.upper() else os.environ[key]}"
            )

        # Parse the request body
        body = json.loads(event["body"])
        text = body["text"]

        # Log OpenAI API key presence (not the key itself)
        api_key = os.environ.get("OPENAI_API_KEY")
        logger.info(f"OpenAI API key present: {api_key is not None}")
        logger.info(f"OpenAI API key length: {len(api_key) if api_key else 0}")

        if not api_key:
            raise ValueError(
                "OpenAI API key not found in environment variables")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Call OpenAI API
        logger.info("Making request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a medical assistant tasked with extracting structured medication information and generating SIG codes.
For each medication, provide a JSON object with the following fields:
- medication: The name of the medication
- sig_code: The standardized SIG code (e.g., "1 tab PO QD" for "Take 1 tablet by mouth daily")
- dosage: The medication dosage (e.g., "500 mg")
- frequency: How often to take the medication (e.g., "every 8 hours", "once daily")
- quantity: The total amount prescribed (e.g., "30 tablets")
- refills: Number of refills or "None"
- purpose: The purpose of the medication if specified, or null if not provided

Format the output as a JSON array of objects. Use standard medical abbreviations in the sig_code:
- PO: by mouth
- QD: once daily
- BID: twice daily
- TID: three times daily
- QID: four times daily
- Q#H: every # hours
- PRN: as needed
- TAB: tablet
- CAP: capsule""",
                },
                {"role": "user", "content": text},
            ],
            response_format={"type": "json_object"},
        )

        # Process the response
        standardized_text = json.loads(response.choices[0].message.content)
        logger.info("Successfully received response from OpenAI")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"text": standardized_text, "status": "success"}),
        }

    except openai.APIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {"error": f"OpenAI API Error: {str(e)}", "status": "error"}
            ),
        }
    except ValueError as e:
        logger.error(f"Value error: {e}")
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": str(e), "status": "error"}),
        }
    except Exception as e:
        logger.error("Unexpected error occurred", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "error": "An unexpected error occurred. Please check the logs.",
                    "status": "error",
                }
            ),
        }
