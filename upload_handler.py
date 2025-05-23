import json
import base64
import boto3
import uuid
import os

s3 = boto3.client('s3')
bucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        body = event['body']
        if event.get("isBase64Encoded", False):
            body = base64.b64decode(body).decode()

        file_content = body
        file_id = str(uuid.uuid4()) + ".txt"

        s3.put_object(Bucket=bucket, Key=f"uploads/{file_id}", Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded", "filename": file_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }