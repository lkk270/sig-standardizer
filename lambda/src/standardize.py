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
            model="chatgpt-4o-latest",
            messages=[
                {
                    "role": "system",
                    "content": """You are a medical assistant tasked with extracting structured medication information and generating SIG codes.
                        For each medication, provide a **strictly valid JSON** array of objects. Do not include any additional text, explanations, or comments.
                        The output must start with '[' and end with ']', containing only the JSON array.

                        Each object in the array should have the following fields:
                        - medication: The name of the medication
                        - sig_code: The standardized SIG code
                        - dosage: The medication dosage
                        - frequency: How often to take the medication
                        - quantity: The total amount prescribed
                        - refills: Number of refills or "None"
                        - purpose: The purpose of the medication if specified, or null if not provided.

                        Example output:
                        [
                            {
                                "medication": "Amoxicillin",
                                "sig_code": "1 CAP PO Q8H",
                                "dosage": "500 mg",
                                "frequency": "every 8 hours",
                                "quantity": "30 capsules",
                                "refills": "None",
                                "purpose": null
                            }
                        ]
                        """,
                },
                {"role": "user", "content": text}
            ]
        )

        # Process the response
        try:
            response_text = response.choices[0].message.content.strip()
            standardized_text = json.loads(response_text)
            logger.info(
                "Successfully received and parsed response from OpenAI")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise ValueError("Invalid JSON response from OpenAI") from e

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
