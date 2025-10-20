# Import the required AWS SDK (boto3) and CSV module
import boto3
import csv

# Define the Lambda handler — this runs automatically when S3 event triggers
def lambda_handler(event, context):
    # Create an S3 client to interact with your S3 bucket
    s3 = boto3.client('s3')

    # Create a DynamoDB resource to insert data into the table
    dynamodb = boto3.resource('dynamodb')

    # Connect to the DynamoDB table named 'CustomerData'
    table = dynamodb.Table('CustomerData')

    # Loop through each record that triggered the Lambda function
    for record in event['Records']:
        # Get the bucket name and file name (object key) from the event
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        # Get the file content from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # Read and decode the file content (bytes → string), then split by lines
        content = response['Body'].read().decode('utf-8').splitlines()

        # Use csv.DictReader to read CSV rows as dictionaries (key-value pairs)
        reader = csv.DictReader(content)

        # Loop through each row in the CSV file
        for row in reader:
            # Insert each row into DynamoDB as a new item
            table.put_item(Item=row)

    # Print success message to CloudWatch logs
    print("Data inserted from S3 into DynamoDB successfully.")
