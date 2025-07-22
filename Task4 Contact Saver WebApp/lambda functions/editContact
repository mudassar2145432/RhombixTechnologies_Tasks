import boto3
import json
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactMessages')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        name = body['name']
        message = body['message']
        submittedAt = datetime.datetime.utcnow().isoformat()

        table.update_item(
            Key={'email': email},
            UpdateExpression="SET #nm = :n, message = :m, submittedAt = :s",
            ExpressionAttributeNames={'#nm': 'name'},
            ExpressionAttributeValues={
                ':n': name,
                ':m': message,
                ':s': submittedAt
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Contact updated'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
