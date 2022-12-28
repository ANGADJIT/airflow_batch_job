<h1>Transaction Analytics Batch Job</h1>
<img src="https://user-images.githubusercontent.com/67195682/209856622-fd760a0f-51ce-4cc5-bd82-a973604a1cb9.png" alt="sorry">
<br>

<h2>Worflow Explaination</h2>
<ol>
    <li>
        There is a mocker script which is generating random 100 transactions every second . This transactions will be
        stored temporarily in assets/temp folder. after every 1 seccond file will be opened in append mode after adding
        the transaction size of file is checked if size of files 6mb then this file will be uploaded in s3 and meta data
        of that file like file name and boolean 'is_processed=false' is added to postgres db.
    </li>
    <li>Parallelly airflow is running which will schedule a dag after every 30 minutes.The task of dag is to submit the
        spark job using livy rest api.</li>
    <li>After dag submit the spark job files will get loaded from hdfs like *.egg and some dependencies. First that job
        query a table from postgres named file_audit_entity and query the all files which is not processed yet. this
        include name of file_name .Then this file_names is used to get all the files from s3.After getting all the file
        this files will get combined in one .txt file this file will loaded into a dataframe after converting into
        dataframe we will perform some queries .
    <li>After performing queries writin this data into a pdf and uploading to back into s3 bucket. after uploading the
        pdf report updating the table attribute 'is_processed'=true
</ol>
<br>
<img src="https://user-images.githubusercontent.com/67195682/209856989-178b5a2e-09e0-4c29-84c9-f56c634dd60e.png">
<br>
<h2>Project dependencies</h2>
<ol>
    <li>
        Hadoop 2.9.x
    </li>
    <li>
        Spark 3.3.0
    </li>
    <li>
        Apache livy 0.7.1
    </li>
    <li>
        Docker
    </li>
</ol>
<br>
<h2>Setup Project</h2>
<ol>
    <li>
        This project used python 3.9.7 so we have to setup that first. there is script in scripts folder named as
        setup-python.bash run that script using bash script/setup-python.bash
    </li>
    <li>
        Create and activate the pyenv enviroment using pyenv virtualenv 3.9.7 [env_name]
    </li>
    <li>
        After we have install dependencies. using pip install -r requirements.txt --no-cache-dir
    </li>
    <li>
        Now we have setup the airflow so we have run airflow-setup script using bach scripts/airflow-setup.bash
    </li>
    <li>
        create a .env file in root of project
        and paste this
        <ol>
            AWS_ACCESS_KEY_ID=[ur-access-key]<br>
            AWS_SECRET_KEY_ID=[ur-secrep-key]<br>
            AWS_REGION=[ur-region]<br>
            DEV_BUCKET_NAME=[ur-s3-bucket-name]<br>
            HOST=[UR-HOST]<br>
            USERNAME=[UR-USERNAME]<br>
            PASSWORD=[UR-PASSWORD]<br>
            DATABASE=[UR-DATABASE]<br>
            PORT=[UR-PORT]<br>
            FILE_SIZE=6664093
        </ol>
    </li>
</ol>
<br>
<h2>How to run the project</h2>
<ol>
    <li>
        start all services
        <ol>
            <li>$HADOOP_HOME/start-all.sh</li>
            <li>$SPARK_HOME/start-all.sh</li>
            <li>$LIVY_HOME/bin/livy-server</li>
        </ol>
    </li>
    <li>
        start airflow using bash scripts/start-airflow.sh
    </li>
    <li>
        run a postgres image in docker
    </li>
    <li>
        run mock_stream_gpay_transaction_data_producer.py file
    </li>
    <li>
        go to airflow and start the spark-job-submit dag
    </li>

</ol>