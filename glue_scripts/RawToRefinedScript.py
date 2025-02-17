import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from datetime import datetime

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','s3inputpath','s3outputpath'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# input parameters to the job
s3inputpath=args['s3inputpath']
s3outputpath=args['s3outputpath']

#current Date
current_date = datetime.now().strftime('%Y-%m-%d')

#Read Today Raw data to ingest into the Refined
df= spark.read.option("multiline", "true").json(s3inputpath+current_date)

#add current date column to the dataframe
df2 = df.withColumn('current_date', F.expr(current_date))

#logging no of records
print(f'Total number of Recors to Refined Tofay:{df2.count()}')

#ingestioning to Refined Path
df2.write.mode("overwrite").parquet(s3outputpath+current_date)

print('ingestion to refined completed')

job.commit()