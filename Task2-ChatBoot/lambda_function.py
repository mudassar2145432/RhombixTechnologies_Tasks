import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "bloom-bot-data"
FILE_NAME = "flower_shop_intents.json"

def lambda_handler(event, context):
    # User's question from Lex
    query = event['inputTranscript'].lower()

    # Load the JSON from S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    faq_data = json.loads(response['Body'].read().decode('utf-8'))

    # Simple matcher
    for key, value in faq_data.items():
        if isinstance(value, dict):
            for flower, answer in value.items():
                if flower in query:
                    return {"messages": [{"contentType": "PlainText", "content": answer}]}
        else:
            if key in query:
                return {"messages": [{"contentType": "PlainText", "content": value}]}

    return {
        "messages": [{
            "contentType": "PlainText",
            "content": "Sorry, I didn’t understand that. Try asking about flower prices, delivery, or shop hours."
        }]
    }

