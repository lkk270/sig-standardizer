import json
import base64
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import io
import os


def preprocess_image(image_bytes):
    """
    Preprocess the image for better OCR results.

    Steps:
    1. Convert to grayscale (PIL)
    2. Contrast enhancement
    3. Resize to enlarge text details
    4. Apply mild blur (optional)
    """
    # --- Load image into PIL ---
    pil_img = Image.open(io.BytesIO(image_bytes)).convert('L')

    # --- Increase contrast slightly ---
    enhancer = ImageEnhance.Contrast(pil_img)
    # Tweak factor (e.g. 1.5, 2.0, 2.5) to see what works best
    pil_img = enhancer.enhance(2.0)

    # --- Resize (double the size) with LANCZOS ---
    pil_img = pil_img.resize(
        (pil_img.width * 2, pil_img.height * 2),
        Image.LANCZOS
    )

    # --- Apply mild blur (optional) ---
    pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=0.5))

    return pil_img


def lambda_handler(event, context):
    """
    AWS Lambda handler to extract text from an image using Tesseract OCR.
    """
    try:
        if 'body' not in event:
            raise ValueError("No body in event")

        # Parse the body
        body = json.loads(event['body']) if isinstance(
            event['body'], str) else event['body']

        if not body.get('image'):
            raise ValueError("No image data provided")

        image_parts = body['image'].split(',')
        if len(image_parts) != 2:
            raise ValueError("Invalid image data format")

        # Decode base64 image data
        image_data = image_parts[1]
        image_bytes = base64.b64decode(image_data)

        # Preprocess the image
        processed_image = preprocess_image(image_bytes)

        # Configure Tesseract environment
        os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
        os.environ['TESSDATA_PREFIX'] = '/opt/lib/tessdata'
        pytesseract.pytesseract.tesseract_cmd = '/opt/bin/tesseract'

        # Tesseract configuration
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
