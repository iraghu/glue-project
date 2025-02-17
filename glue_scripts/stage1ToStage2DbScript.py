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
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# input parameters to the job



s3_client = boto3.client('s3')
response = s3_client.get_object(Bucket='triglamda', Key='creds.json')
creds = json.loads(response['Body'].read().decode('utf-8'))

# Read data from PostgreSQL table using JDBC
jdbc_url = "jdbc:postgresql://rdstestinstance.c7am2q24ao0o.ap-south-1.rds.amazonaws.com:5432/rdstestdb"

query ="SELECT a.name, a.address,a.state, a.zip, b.END_GRADE FROM private a, public b where a.ncesid='01433634' and a.ENROLLMENT > '200' limit 5"


properties = creds[0]

#load data from the Db 
table1Df = spark.read.jdbc(url=jdbc_url, table='stage1.private_schools', properties=properties)

#create or Replace Table a
table1Df.createOrReplaceTempView("private")

#load data from the Db
table2Df = spark.read.jdbc(url=jdbc_url, table='stage1.public_schools', properties=properties)

#create or Replace the Table b
table2Df.createOrReplaceTempView("public")

tableoutputDF=spark.sql(query)

#print(f'Total number of Recors to Refined Tofay:{tableoutputDF.count()}')

# PostgreSQL connection properties
#jdbc_url_target = "jdbc:postgresql://rdsrefinedcluster.cluster-c7am2q24ao0o.ap-south-1.rds.amazonaws.com:5423/postgres"


# Write DataFrame to PostgreSQL

tableoutputDF.write.jdbc(url=jdbc_url, table='stage2.schools_reserch', mode="overwrite", properties=properties)

print('ingestion to refined completed')

job.commit()