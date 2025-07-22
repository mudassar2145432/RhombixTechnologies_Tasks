import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactMessages')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        
        item = {
            'email': data['email'],
            'name': data['name'],
            'message': data['message'],
            'submittedAt': datetime.utcnow().isoformat()
        }

        # Prevent overwrite: Only insert if email doesn't already exist
        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(email)'
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Contact saved successfully!'})
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Email already exists!'})
            }
        else:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Could not save message', 'details': str(e)})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Invalid input', 'details': str(e)})
        }
