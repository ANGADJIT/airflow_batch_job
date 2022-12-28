from setuptools import setup

setup(
    name='make-report-job',
    version='1.0',
    packages=['jobs'],
    install_requires=[
        'pyspark','boto3','psycopg2','weasyprint','python-dotenv'
    ]
)
