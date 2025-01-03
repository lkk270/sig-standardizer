import json
import base64
import pytesseract
from PIL import Image, ImageFilter, Resampling  # <-- import Resampling
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
    image = image.resize(
        (image.width * 2, image.height * 2),
        Resampling.LANCZOS  # <-- use Resampling.LANCZOS instead of Image.ANTIALIAS
    )
    # Apply Gaussian blur for noise reduction
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    return image


def lambda_handler(event, context):
    try:
        print("Step 1: Checking event body")
        if 'body' not in event:
            raise ValueError("No body in event")

        print("Step 2: Parsing event['body']")
        body = json.loads(event['body']) if isinstance(
            event['body'], str) else event['body']

        print("Step 3: Checking for image in body")
        if not body.get('image'):
            raise ValueError("No image data provided")

        print("Step 4: Splitting base64 data")
        image_parts = body['image'].split(',')
        if len(image_parts) != 2:
            raise ValueError("Invalid image data format")

        image_data = image_parts[1]
        image_bytes = base64.b64decode(image_data)

        print("Step 5: Preprocessing image")
        processed_image = preprocess_image(image_bytes)

        print("Step 6: Setting Tesseract environment variables")
        os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
        os.environ['TESSDATA_PREFIX'] = '/opt/lib/tessdata'
        pytesseract.pytesseract.tesseract_cmd = '/opt/bin/tesseract'

        print("Step 7: Checking Tesseract version")
        version = pytesseract.get_tesseract_version()
        print("Tesseract version:", version)

        print("Step 8: Calling pytesseract.image_to_string")
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(
            processed_image, config=custom_config
        )

        print("Step 9: Returning OCR result")
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
        print("Exception caught:", error_details)

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
