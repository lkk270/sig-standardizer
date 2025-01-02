import json
import base64
import pytesseract
from PIL import Image
import io
import os

# Set LD_LIBRARY_PATH to find shared libraries
os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
pytesseract.pytesseract.tesseract_cmd = '/opt/lib/tesseract'


def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])

        # Get the base64 encoded image
        # Remove data:image/jpeg;base64,
        image_data = body['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # Open the image using PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'text': extracted_text,
                'status': 'success'
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # For CloudWatch logs
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
