import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from datetime import datetime
import boto3
import json
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','s3inputpath','table'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# input parameters to the job  SHELTER_ID
s3inputpath=args['s3inputpath']
refinedtable=args['table']

s3_client = boto3.client('s3')
response = s3_client.get_object(Bucket='triglamda', Key='creds.json')
creds = json.loads(response['Body'].read().decode('utf-8'))

#current Date
current_date = datetime.now().strftime('%Y-%m-%d')

#Read Today Raw data to ingest into the Refined
#df= spark.read.option("multiline", "true").json(s3inputpath)
df = spark.read.format("csv").option("header", "true").load(s3inputpath+current_date)
df2= df.drop("SHELTER_ID")

#add current date column to the dataframe
#df2 = df.withColumn('current_date', F.expr(current_date))

#logging no of records
print(f'Total number of Recors to Refined Tofay:{df2.count()}')

# PostgreSQL connection properties
jdbc_url = "jdbc:postgresql://rdstestinstance.c7am2q24ao0o.ap-south-1.rds.amazonaws.com:5432/rdstestdb"
properties = creds[0]

# Write DataFrame to PostgreSQL
df2.write.jdbc(url=jdbc_url, table=refinedtable, mode="overwrite", properties=properties)



#ingestioning to Refined Path
#df2.write.mode("overwrite").parquet(s3outputpath+current_date)

print('ingestion to refined completed')

job.commit()