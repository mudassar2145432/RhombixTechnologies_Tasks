import boto3
import uuid
import json

def lambda_handler(event, context):
    # Parse the body if coming from API Gateway
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }

    # Set the DynamoDB resource and use the new table name 'BloodBankTable'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BloodBankTable')  # Updated table name

    try:
        table.put_item(
            Item={
                'deposit_id': str(uuid.uuid4()),  # Generate a unique deposit ID
                'blood_type': body['blood_type'],
                'storage_area': body['storage_area'],
                'storage_date': body['storage_date'],
                'depositor_name': body['depositor_name'],
                'depositor_contact': body['depositor_contact'],
                'patient_name': body['patient_name'],
                'patient_contact': body['patient_contact'],
            }
        )
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing required field: {str(e)}'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Blood deposit added successfully.'})
    }
