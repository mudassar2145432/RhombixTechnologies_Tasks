import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactMessages')

def lambda_handler(event, context):
    try:
        items = []
        response = table.scan()
        items.extend(response.get('Items', []))

        # Continue scanning if there is more data
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        # Sort items by submittedAt (newest first)
        sorted_items = sorted(items, key=lambda x: x['submittedAt'], reverse=True)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(sorted_items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Could not fetch contacts', 'details': str(e)})
        }
