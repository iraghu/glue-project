import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from datetime import datetime

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','s3inputpath','s3outputpath','columns'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


#input arguments to read write the table data
s3inputpath=args['s3inputpath']
s3outputpath=args['s3outputpath']
columns=args['columns']

#list of columns selected to the processed zone
columnslist = columns.split(',')

#current date extraction
current_date = datetime.now().strftime('%Y-%m-%d')

#ingesting today's  refined table data into the  processed zone
print(f'ingesting today {current_date}  refined table data into the  processed zone')
df= spark.read.parquet(s3inputpath+current_date)
print(f'reading from the refined zone completed: {s3inputpath+current_date} ')


#selected  columns to the processed zone
print(f'selected columns ingesting to processed zone {columnslist} ')
df2=df.selectExpr(columnslist)

print(f'number of Records to processed zone:{df2.count()}')
df2.write.mode("overwrite").parquet(s3outputpath+current_date)
print(f'writing to the processed zone completed: {s3outputpath+current_date} ')

job.commit()