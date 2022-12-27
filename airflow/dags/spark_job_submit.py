from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import json
from os import environ

default_agrs: dict = {
    'owner': 'angadjit-singh',
    'retries': 5,
    'retry_delay': timedelta(seconds=5)
}


@dag(
    dag_id='spark-job-submit',
    start_date=datetime(year=2022,day=26,month=12),
    description='This dag runs after every 30 minutes and submit the job to livy server',
    schedule_interval=timedelta(minutes=30),
    default_args=default_agrs,
    catchup=False
)
def spark_job_submit():

    @task()
    def get_elastic_ip() -> str:
        if environ.get('USER') != 'angad':
            return 'http://3.7.15.253:8998/batches'

        return 'http://localhost:8998/batches'

    @task()
    def submit_job(ip: str) -> None:
        data: dict = {
            'file': '/jobs/make-report.py',
            'pyFiles': ['/jobs/make_report_job-1.0-py3.9.egg', '/jobs/template_string.py']
        }

        requests.post(ip, data=json.dumps(data))

    ip: str = get_elastic_ip()
    submit_job(ip)


submit = spark_job_submit()
