import os
import pymysql.cursors
import logging

DEFAULT_DB_HOST = 'localhost'

def get_conn():
    host = os.environ.get('HZPORTAL_DB_HOST', DEFAULT_DB_HOST)
    user = os.environ.get('HZPORTAL_DB_USER')
    pw = os.environ.get('HZPORTAL_DB_PW')
    db = os.environ.get('HZPORTAL_DB_NAME')
    if host == DEFAULT_DB_HOST:
        logging.info('db connection attempting to use default host: %s' % DEFAULT_DB_HOST)
    if not user:
        raise RuntimeError('Please set HZPORTAL_DB_USER')
    if not pw:
        raise RuntimeError('Please set HZPORTAL_DB_PW')
    if not db:
        raise RuntimeError('Please set HZPORTAL_DB_NAME')

    return pymysql.connect(
        host=host,
        user=user,
        password=pw,
        db=db,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )