from api.interface_log import Interface
from utils.data_helpers import get_yamldata
from configs.config import config
from utils.api_assertions import assertions
from utils.mylog import Logger
import pytest
import pymysql

logger=Logger('money').get_logger()

client=Interface('http://localhost:90')

yaml_file=r'D:\untitled1\lessons\test_data\smoke_test_data.yaml'


@pytest.fixture(scope='session')
def db_fixture():
    connect=pymysql.connect(database='finance',autocommit=True,**config.LOCAL_DATABASE)
    cursor=connect.cursor()
    yield cursor,connect

    if cursor:
        cursor.close()
    if connect:
        connect.close()

@pytest.mark.smoke
class TestCase:

    @pytest.mark.parametrize('url,params,b_code,uid,username',get_yamldata(yaml_file).get('register'))
    def test_register(self,db_fixture,url,params,b_code,uid,username):
        cur, con = db_fixture
        cur.execute('delete from user where id=%s or username=%s',(uid, username))  # 测试前，清理数据

        http_code, json_dat = client.post(url, **params).values()
        assertions.assert_code(http_code, 200)
        assertions.assert_jsondata(json_dat, 'code', b_code)

        cur.execute('update user set id=%s where username=%s', (uid, username))  # 更改用户的id

    @pytest.mark.parametrize('url,params,h_code,b_code',get_yamldata(yaml_file).get('login'))
    def test_login(self,url,params,h_code,b_code):
        http_code,json_dat=client.get(url,**params).values()
        assertions.assert_code(http_code,h_code)
        assertions.assert_jsondata(json_dat,'code',b_code)

    @pytest.mark.parametrize('url,params,b_code',get_yamldata(yaml_file).get('updateUserProfile'))
    def test_updateUserProfile(self,url,params,b_code):
        http_code, json_dat = client.put(url, **params).values()
        assertions.assert_code(http_code, 200)
        assertions.assert_jsondata(json_dat, 'code', b_code)

"""
下面的测试函数，可以参考

"""

    # @pytest.mark.parametrize('url,params,h_code,b_code',get_yamldata(yaml_file).get('login'))
    # def test_login(self,url,params,h_code,b_code):
    #     http_code,json_dat=client.get(url,**params).values()
    #     assertions.assert_code(http_code,h_code)
    #     assertions.assert_jsondata(json_dat,'code',b_code)
    #
    # @pytest.mark.parametrize('url,params,h_code,b_code,username,shop_price',get_yamldata(yaml_file).get('buy'))
    # def test_buy(self,db_fixture,url,params,h_code,b_code,username,shop_price):
    #
    #     cursor,connect=db_fixture  # 获取游标，连接
    #     sql="select b.balance from user u,bankcard b WHERE u.id=b.userId and u.username=%s AND b.defaultl=1"
    #
    #     cursor.execute(sql,(username,))
    #     before_money =cursor.fetchone()[0]   # 获取查询前的账户金额
    #     logger.info(f'购买前金额为：{before_money}')
    #
    #     http_code, json_dat = client.post(url, **params).values()  # 发送请求
    #
    #     cursor.execute(sql,(username,))
    #     after_money=cursor.fetchone()[0]  # 获取购买理财后的账户金额
    #     logger.info(f'购买后金额为：{after_money}')
    #
    #
    #     assertions.assert_code(http_code, h_code)
    #     assertions.assert_jsondata(json_dat, 'code', b_code)
    #     assert before_money-shop_price ==after_money  # 断言金额





