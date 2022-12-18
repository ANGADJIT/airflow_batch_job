from model.gpay_transaction_model import GPayTransaction
from aws.s3_functions import upload_file
from os import stat, mkdir
from os.path import exists
from db.file_audit import *
import sched
import time

# main AIM of setup func is to create important assets dir's
def setup() -> None:
    if exists('mock/assets') == False:
        mkdir('mock/assets')
        mkdir('mock/assets/temp')


def main(sc) -> None:
    with open('mock/assets/temp/transactions.txt', 'a') as txt_file:
        # appending 100 records at every 1 second
        transactions: list[str] = [str(GPayTransaction()) for _ in range(100)]
        txt_file.writelines(transactions)

    # check file size not more then 66_64_093 bytes
    size: int = stat('mock/assets/temp/transactions.txt').st_size

    # upload file to S3 and insert record if file size is more than 66_64_093 bytes
    if size >= int(environ.get('FILE_SIZE')):
        file_name: str = insert_file_audit()
        upload_file(object_name=file_name)

    sc.enter(1, 1, main, (sc,))


if __name__ == '__main__':
    setup()

    # run after every 1 second
    s = sched.scheduler(time.time, time.sleep)

    s.enter(1, 1, main, (s,))
    s.run()
