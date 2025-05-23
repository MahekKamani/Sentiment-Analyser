import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        filename = event['filename']
        summary = event['summary']
        timestamp = datetime.utcnow().isoformat()

        table.put_item(
            Item={
                'FileName': filename,
                'Summary': summary,
                'Timestamp': timestamp
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Saved to DynamoDB"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }