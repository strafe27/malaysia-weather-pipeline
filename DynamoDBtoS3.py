import json
import boto3
import csv
from io import StringIO
from datetime import datetime, timedelta

# Initialize AWS clients
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Example: Retrieve data from DynamoDB table using pagination
        table_name = 'weather'
        scan_params = {
            'TableName': table_name,
            # Add more parameters like FilterExpression, ProjectionExpression, etc., as needed
        }
        
        dynamodb_response = []
        while True:
            response = dynamodb.scan(**scan_params)
            dynamodb_response.extend(response.get('Items', []))
            # Check if there are more items to fetch
            if 'LastEvaluatedKey' in response:
                scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
            else:
                break
        
        # Example: Prepare data for CSV format
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        
        # Write header based on the keys in the first item (assuming all items have the same keys)
        if dynamodb_response:
            header = dynamodb_response[0].keys()
            csv_writer.writerow(header)
            
            # Write data rows
            for item in dynamodb_response:
                csv_writer.writerow([item[key]['S'] if 'S' in item[key] else item[key]['N'] for key in header])
        
        # Generate Malaysia Time (MYT) timestamp for filename
        current_time_utc = datetime.utcnow()
        current_time_my = current_time_utc + timedelta(hours=8)  # Malaysia is UTC+8
        timestamp_my = current_time_my.strftime('%d-%m-%y_%H-%M-%S')
        
        # Example: Upload data to S3 bucket with Malaysia Time (MYT) timestamped filename
        s3_bucket = 'forsnowflake-v1'
        s3_path = 'snowflake/'
        s3_key = f'{s3_path}weather_{timestamp_my}.csv'  # Using MYT timestamp in the filename
        
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=csv_data.getvalue().encode('utf-8')
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Data uploaded to S3 successfully with Malaysia Time (MYT) timestamped filename: {s3_key}')
        }
    
    except Exception as e:
        print(f'Error: {str(e)}')
        raise e  # Raise the exception to propagate it and trigger Lambda retry or alert