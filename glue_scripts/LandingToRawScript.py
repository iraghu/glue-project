import sys
import json
import boto3
from datetime import datetime
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from awsglue.context import GlueContext
    
args = getResolvedOptions(sys.argv, ['JOB_NAME','landingbucket','landingpath'])
s3_client = boto3.client('s3')
landing_bucket = args['landingbucket']
landingpath=args['landingpath']
print("landingbucket=="+landing_bucket)
print("landingbucket=="+landingpath)
    # Check if there are files in the landing path
response = s3_client.list_objects_v2(Bucket=landing_bucket,Prefix=landingpath)
# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime('%Y-%m-%d')
print("current_date=="+current_date)
if 'Contents' in response and len(response['Contents']) > 0:
        for obj in response['Contents']:
            keyname=obj['Key']
            parts = keyname.split('/')
            subfolder = parts[-2]
            filename=parts[-1]
            destination_key = f"raw/{subfolder}/{current_date}/{filename}"
            s3_client.copy_object(Bucket=landing_bucket,Key=destination_key,
            CopySource={'Bucket': landing_bucket, 'Key': keyname})