import json
import base64
import pytesseract
from PIL import (
    Image,
    ImageFilter,
    ImageEnhance  # For contrast enhancement
)
import io
import os


def preprocess_image(image_bytes):
    """
    Preprocess the image for better OCR results.
    Steps:
    1. Convert to grayscale
    2. Optional thresholding/binarization (commented out by default)
    3. Contrast enhancement
    4. Resize to double the original size using LANCZOS
    5. Apply Gaussian blur to reduce noise
    """
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to grayscale
    image = image.convert('L')

    # [Optional] Binarize the image with a fixed threshold
    # If text is faint or background is inconsistent,
    # try adaptive thresholding in Pillow or test various thresholds.
    #
    # threshold = 128
    # image = image.point(lambda x: 255 if x > threshold else 0, '1')

    # Increase contrast a bit (factor of 1.5 or 2.0 can sometimes help)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Resize to double the original size with LANCZOS filter
    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.LANCZOS
    )

    # Apply a mild Gaussian blur to reduce background noise
    image = image.filter(ImageFilter.GaussianBlur(radius=1))

    return image


def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("No body in event")

        # Parse JSON body
        body = json.loads(event['body']) if isinstance(
            event['body'], str) else event['body']

        if not body.get('image'):
            raise ValueError("No image data provided")

        # Decode base64 image
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

        # Tesseract config:
        # - OEM 3 uses the LSTM engine,
        # - PSM 6 assumes a single uniform block of text.
        # You can experiment with e.g. psm 7, 11, or 12 if text is multiline or irregular.
        custom_config = r'--oem 3 --psm 6'

        # If you only have English, specify lang='eng' for clarity;
        # if you have more languages, e.g. 'eng+spa', install them in your Tesseract layer.
        extracted_text = pytesseract.image_to_string(
            processed_image, config=custom_config
        )

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
