import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        filename = event['pathParameters']['filename']
        response = table.get_item(Key={'FileName': filename})

        if 'Item' in response:
            return {
                "statusCode": 200,
                "body": json.dumps(response['Item'])
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Summary not found"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }