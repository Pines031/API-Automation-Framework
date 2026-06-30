import pytest
from configs.config import config
from logs.mylog import Logger
from unittest.mock import patch
import pymysql

logger=Logger('CONFTEST').getlogger()

@pytest.fixture(scope='session')
def suite():
    logger.info('=' * 80)
    logger.info('Test suite starts'.upper())
    logger.info('=' * 80)
    yield
    logger.info('=' * 80)
    logger.info('Test suite over'.upper())
    logger.info('=' * 80)

@pytest.fixture(scope='session')
def db_fixture():
    connect=pymysql.connect(database='finance',autocommit=True,**config.LOCAL_DATABASE)
    cursor=connect.cursor()
    yield cursor,connect

    if cursor:
        cursor.close()
    if connect:
        connect.close()





