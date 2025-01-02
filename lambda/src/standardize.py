import json
import os
import openai


def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])
        text = body['text']

        # Initialize OpenAI client
        client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Standardize the following signature block format."},
                {"role": "user", "content": text}
            ]
        )

        standardized_text = response.choices[0].message.content

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'text': standardized_text,
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
