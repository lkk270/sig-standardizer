import json
import base64
import pytesseract
from PIL import Image, ImageFilter
import io
import os


def preprocess_image(image_bytes):
    """
    Preprocess the image for better OCR results.
    - Converts to grayscale
    - Resizes for better clarity
    - Applies Gaussian blur to remove noise
    """
    image = Image.open(io.BytesIO(image_bytes))
    # Convert to grayscale
    image = image.convert('L')
    # Resize to double the original size
    image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)
    # Apply Gaussian blur for noise reduction
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    return image


def lambda_handler(event, context):
    """
    AWS Lambda handler to extract text from an image using Tesseract OCR.
    """
    try:
        # Parse and validate the incoming request
        if 'body' not in event:
            raise ValueError("No body in event")

        # Parse the body as JSON
        body = json.loads(event['body']) if isinstance(
            event['body'], str) else event['body']

        if not body.get('image'):
            raise ValueError("No image data provided")

        # Decode the base64 image data
        image_parts = body['image'].split(',')
        if len(image_parts) != 2:
            raise ValueError("Invalid image data format")

        image_data = image_parts[1]
        image_bytes = base64.b64decode(image_data)

        # Preprocess the image
        processed_image = preprocess_image(image_bytes)

        # Configure Tesseract environment
        os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
        os.environ['TESSDATA_PREFIX'] = '/opt/lib/tessdata'
        pytesseract.pytesseract.tesseract_cmd = '/opt/bin/tesseract'

        # Perform OCR using Tesseract with optimized configurations
        custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode and Page Segmentation Mode
        extracted_text = pytesseract.image_to_string(
            processed_image, config=custom_config)

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
        # Capture and return detailed error information
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'error_details': getattr(e, 'args', [])
        }

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'error_details': error_details,
                'status': 'error'
            })
        }
