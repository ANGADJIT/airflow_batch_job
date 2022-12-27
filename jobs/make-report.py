from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType
from pyspark.sql import SparkSession
from dotenv import dotenv_values
import psycopg2
import boto3
from template_string import make_template_string
from pyspark.sql import DataFrame
from weasyprint import HTML
from tempfile import NamedTemporaryFile
from datetime import datetime


def to_record_tuple(record_str: str) -> tuple:
    '''This cast fields in correct data types and make a tuple of it'''
    record: list[str] = record_str.split(',')

    return (record[0], float(record[1]), record[2], record[3], int(record[4]), int(record[5]), record[6], int(record[7]))


spark: SparkSession = SparkSession.builder.appName(
    'Transactions Report').getOrCreate()

# Data Model for transaction
transaction_schema: StructType = StructType(fields=[
    StructField(name='id', dataType=StringType(), nullable=False),
    StructField(name='amount', dataType=FloatType(), nullable=False),
    StructField(name='bank', dataType=StringType(), nullable=False),
    StructField(name='state', dataType=StringType(), nullable=False),
    StructField(name='hour', dataType=IntegerType(), nullable=False),
    StructField(name='minute', dataType=IntegerType(), nullable=False),
    StructField(name='status', dataType=StringType(), nullable=False),
    StructField(name='transaction_time',
                dataType=IntegerType(), nullable=False),
])


# loading db and AWS cred
env = dotenv_values('.env')

conn = psycopg2.connect(host=env['HOST'],
                        port=env['PORT'],
                        database=env['DATABASE'],
                        password=env['PASSWORD'],
                        user=env['USERNAME'])

cursor = conn.cursor()

# get all files to be processed

query: str = 'select file_name from file_audit_enitity where is_processed = false'

cursor.execute(query)

results = [dict(line) for line in [zip(
    [column[0] for column in cursor.description], row) for row in cursor.fetchall()]]

file_names = [result['file_name'] for result in results]

# get all file from S3 for processing
s3 = boto3.client(service_name='s3', region_name=env['AWS_REGION'],
                  aws_access_key_id=env['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=env['AWS_SECRET_KEY_ID'])

bucket = s3.list_objects(Bucket=env['DEV_BUCKET_NAME'])

files: list[str] = []

for obj in bucket.get('Contents'):

    if obj['Key'] in file_names:
        data = s3.get_object(Bucket=env[
            'DEV_BUCKET_NAME'], Key=obj.get('Key'))
        contents = data['Body'].read()

        files.append(contents.decode('utf-8'))

combined: str = '\n'.join(files)

combined_typed: list[tuple] = [to_record_tuple(
    record) for record in combined.split('\n') if len(record)]
transactions: DataFrame = spark.createDataFrame(
    combined_typed, schema=transaction_schema)

# register view in temp tables and query from it
transactions.createOrReplaceTempView('transactions')

# Query 1: Get state name with highest number of success count

query1: DataFrame = spark.sql(
    "SELECT state,count(status) as count from transactions where status='SUCCESS' group by state order by count desc limit 1")

q1_result: dict = query1.collect()[0].asDict()

# Query 2 : Get state with highest average amount of transaction for successful transactions

query2: DataFrame = spark.sql(
    "select state,round(avg(amount),2) as average from transactions where status='SUCCESS' group by state order by average desc limit 1")

q2_result: dict = query2.collect()[0].asDict()

# make a pdf report and upload to S3
html = NamedTemporaryFile()

data: dict = {
    'state-q1': q1_result['state'],
    'state-q2': q2_result['state'],
    'count': q1_result['count'],
    'average': q2_result['average'],
}

html.write(bytes(f'{make_template_string(data)}', 'utf-8'))
html.flush()

file = NamedTemporaryFile()

HTML(html.name).write_pdf(file.name)

now = datetime.now()
timestamp: str = f'{now.day}-{now.month}-{now.year}_{now.hour}:{now.minute}:{now.second}'

s3.upload_file(file.name, env['DEV_BUCKET_NAME'], f'report{timestamp}.pdf')

html.close()

# after pdf uploaded to s3 update the table

update_query: str = f"update file_audit_enitity set is_processed=true where file_name in {tuple(file_names)}"

cursor.execute(update_query)
conn.commit()