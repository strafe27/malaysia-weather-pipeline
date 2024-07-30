import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("weather")

    try:
        # Scan all items in the table
        response = table.scan()
        items = response.get('Items', [])

        # Check if there are items to delete
        if not items:
            return {
                'statusCode': 200,
                'body': 'No items to delete'
            }

        # Delete each item
        with table.batch_writer() as batch:
            for item in items:
                # Delete each item using city and time as keys
                batch.delete_item(Key={
                    'city': item['city'],
                    'time': item['time']
                })

        return {
            'statusCode': 200,
            'body': 'All items deleted successfully'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error deleting items: {str(e)}'
        }
