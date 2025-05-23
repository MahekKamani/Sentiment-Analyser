import json
import boto3
import os

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend', region_name='us-east-1')  # hardcoded

bucket = os.environ['BUCKET_NAME']

def detect_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return {
        "Sentiment": response.get("Sentiment"),
        "SentimentScore": response.get("SentimentScore")
    }

def lambda_handler(event, context):
    try:
        print("Event:", event)

        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        key = body.get('filename')

        if not key:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'filename' in request body"})
            }

        response = s3.get_object(Bucket=bucket, Key=f"uploads/{key}")
        content = response['Body'].read().decode('utf-8')

        sentiment_result = detect_sentiment(content)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "filename": key,
                "sentiment": sentiment_result["Sentiment"],
                "confidence_scores": sentiment_result["SentimentScore"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }