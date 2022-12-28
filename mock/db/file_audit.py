import psycopg2
from dotenv import load_dotenv
from os import environ
from datetime import datetime

load_dotenv()

conn = psycopg2.connect(host=environ.get('HOST'),
                        port=environ.get('PORT'),
                        database=environ.get('DATABASE'),
                        password=environ.get('PASSWORD'),
                        user=environ.get('USERNAME'))

cursor = conn.cursor()


def insert_file_audit() -> str:
    now = datetime.now()
    timestamp: str = f'{now.day}-{now.month}-{now.year}_{now.hour}:{now.minute}:{now.second}'

    file_name: str = f'transactions{timestamp}.txt'

    sql: str = f"INSERT INTO file_audit_enitity (file_name)VALUES('{file_name}')"
    cursor.execute(sql)
    conn.commit()

    return file_name


def close_db() -> None:
    cursor.close()
    conn.close()
