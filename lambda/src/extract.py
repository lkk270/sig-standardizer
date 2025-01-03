import json
import base64
import pytesseract
from PIL import Image, ImageFilter  # Remove Resampling
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
    # Resize to double the original size, using LANCZOS
    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.LANCZOS  # Works in older Pillow versions
    )
    # Apply Gaussian blur for noise reduction
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    return image


def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("No body in event")

        body = json.loads(event['body']) if isinstance(
            event['body'], str) else event['body']

        if not body.get('image'):
            raise ValueError("No image data provided")

        image_parts = body['image'].split(',')
        if len(image_parts) != 2:
            raise ValueError("Invalid image data format")

        image_data = image_parts[1]
        image_bytes = base64.b64decode(image_data)

        processed_image = preprocess_image(image_bytes)

        # Configure Tesseract environment
        os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
        os.environ['TESSDATA_PREFIX'] = '/opt/lib/tessdata'
        pytesseract.pytesseract.tesseract_cmd = '/opt/bin/tesseract'

        custom_config = r'--oem 3 --psm 6'
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
