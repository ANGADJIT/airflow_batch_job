export AIRFLOW_HOME=/home/$USER/airflow_batch_job/airflow
airflow webserver -p 8000 & airflow scheduler