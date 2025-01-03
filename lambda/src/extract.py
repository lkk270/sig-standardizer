import json
import base64
import pytesseract
from PIL import Image
import io
import os
import subprocess


def lambda_handler(event, context):
    try:
        print("=== ENVIRONMENT AND SYSTEM INFO ===")
        # Print all environment variables
        print("\nAll Environment Variables:")
        for key, value in os.environ.items():
            print(f"{key}: {value}")

        print("\n=== DIRECTORY STRUCTURE ===")
        # Check entire /opt directory structure
        print("\nComplete /opt directory tree:")
        try:
            print(subprocess.check_output(
                ['find', '/opt', '-type', 'f'], text=True))
        except Exception as e:
            print(f"Error listing /opt directory: {str(e)}")

        # Check layer contents
        print("\nLayer libraries:")
        try:
            print(subprocess.check_output(
                ['ldd', '/opt/lib/tesseract'], text=True))
        except Exception as e:
            print(f"Error checking libraries: {str(e)}")

        # Check tessdata
        print("\nTessdata contents:")
        try:
            print(subprocess.check_output(
                ['ls', '-l', '/opt/lib/tessdata'], text=True))
        except Exception as e:
            print(f"Error listing tessdata: {str(e)}")

        # Debug: Print environment variables and file structure
        print("Environment variables:")
        print(f"LD_LIBRARY_PATH: {os.environ.get('LD_LIBRARY_PATH')}")
        print(f"TESSDATA_PREFIX: {os.environ.get('TESSDATA_PREFIX')}")
        print(f"PATH: {os.environ.get('PATH')}")

        print("\nDirectory contents:")
        print("/opt contents:")
        print(subprocess.check_output(['ls', '-lR', '/opt']).decode())

        print("\nTesseract binary check:")
        tesseract_path = '/opt/lib/tesseract'
        if os.path.exists(tesseract_path):
            print(f"Tesseract exists at {tesseract_path}")
            print(
                f"File permissions: {oct(os.stat(tesseract_path).st_mode)[-3:]}")
        else:
            print(f"Tesseract not found at {tesseract_path}")

        # Set environment variables for Tesseract
        os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
        os.environ['TESSDATA_PREFIX'] = '/opt/lib/tessdata'
        pytesseract.pytesseract.tesseract_cmd = '/opt/bin/tesseract'

        # Parse the request body
        body = json.loads(event['body'])

        # Get the base64 encoded image
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
        print(f"Error: {str(e)}")
        # If it's a subprocess error, print the output
        if isinstance(e, subprocess.CalledProcessError):
            print(f"Command output: {e.output.decode()}")
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
