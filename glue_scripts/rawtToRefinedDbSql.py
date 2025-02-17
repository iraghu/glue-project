import json
import boto3
import os
import pg8000
from awsglue.utils import getResolvedOptions
import sys

    # Get S3 event details
args = getResolvedOptions(sys.argv, ['JOB_NAME','bucket_name','tablename'])
bucket_name = args['bucket_name']
tablename=args['tablename'] 
rawpath=f'raw/{tablename}'
    # Connect to the PostgreSQL Database

conn = pg8000.connect(
            database="rdstestdb",
            user="quad",
            password="quad1777",
            host="rdstestinstance.c7am2q24ao0o.ap-south-1.rds.amazonaws.com",
            port="5432"
        )
cursor = conn.cursor()

        # S3 Client to fetch the file from S3
s3_client = boto3.client('s3')
response = s3_client.list_objects_v2(Bucket=bucket_name,Prefix=rawpath)
for obj in response['Contents']:
            if "json" in obj['Key']:

                print(f"Object: {obj['Key']}")

                file_obj = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
                 # Read the JSON file from S3
                file_content = file_obj['Body'].read().decode('utf-8')
                json_data = json.loads(file_content)  # Assuming the file is in JSON format

                 
                        
                for record in json_data:
                # Dynamically create columns and values for the INSERT statement
                      columns = ', '.join(record.keys())
                      values = ', '.join([f"%s" for _ in record.values()])
                      query = f"INSERT INTO employeeDuplicate ({columns}) VALUES ({values})"

                # Execute the dynamic query
                cursor.execute(query, tuple(record.values()))

        # Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

        
