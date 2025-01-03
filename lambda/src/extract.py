import json
import base64
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import io
import os

# If using deskew or thresholding, you'll need OpenCV:
import cv2
import numpy as np


def preprocess_image(image_bytes):
    """
    Preprocess the image for better OCR results.

    Steps:
    1. Convert to grayscale (PIL)
    2. (Optional) Deskew using OpenCV
    3. Adaptive thresholding in OpenCV
    4. Convert back to PIL
    5. Contrast enhancement
    6. Resize to enlarge text details
    7. Apply mild blur (optional)
    """
    # --- Load image into PIL ---
    pil_img = Image.open(io.BytesIO(image_bytes)).convert('L')

    # --- Convert PIL -> OpenCV (NumPy array) ---
    cv_img = np.array(pil_img)

    # --- (Optional) Deskew ---
    # Uncomment to test deskew if your images are noticeably skewed
    # coords = np.column_stack(np.where(cv_img > 0))
    # angle = cv2.minAreaRect(coords)[-1]
    # if angle < -45:
    #     angle = -(90 + angle)
    # else:
    #     angle = -angle
    # (h, w) = cv_img.shape[:2]
    # center = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # cv_img = cv2.warpAffine(cv_img, M, (w, h),
    #                         flags=cv2.INTER_CUBIC,
    #                         borderMode=cv2.BORDER_REPLICATE)

    # --- Adaptive Thresholding ---
    # Use cv2.ADAPTIVE_THRESH_GAUSSIAN_C or cv2.ADAPTIVE_THRESH_MEAN_C
    # Larger blockSize for bigger text areas; tweak 'C' as needed.
    cv_img = cv2.adaptiveThreshold(
        cv_img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,    # blockSize
        8      # C (constant subtracted from the mean)
    )

    # --- Convert back to PIL ---
    pil_img = Image.fromarray(cv_img)

    # --- Increase contrast slightly ---
    enhancer = ImageEnhance.Contrast(pil_img)
    # Tweak factor (e.g. 1.5, 2.0, 2.5) to see what works best
    pil_img = enhancer.enhance(2.0)

    # --- Resize (double the size) with LANCZOS ---
    # LANCZOS works for older and newer Pillow as Image.LANCZOS
    pil_img = pil_img.resize(
        (pil_img.width * 2, pil_img.height * 2),
        Image.LANCZOS
    )

    # --- Apply mild blur (optional) ---
    # For handwritten text, too much blur can remove details. Tweak radius or comment out if it hurts recognition.
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
        # Try other psm modes for better multiline or irregular text: e.g. 7, 11, 12
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
