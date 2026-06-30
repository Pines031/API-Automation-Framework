from unittest.mock import patch
import requests
from utils.data_helpers import database_helper
from configs.config import config

"""
1.注册用户名长度，不能小于6
2.注册用户名不能重复

"""

def mock_register(*args,**kwargs):

    class MyRequest:

        def __init__(self):
            self.status_code=200
            self.text='123456789'

        def json(self):

            user_name=kwargs.get('data').get('username')  # 获取接口的用户名

            user_list=[i[0] for i in database_helper('select username from user',**config.LOCAL_DATABASE)]  # 从数据库获取存量用户名

            # 需求校验（模拟）
            if len(user_name)<6:
                return {"code":202,"msg":"注册用户名长度，不能小于6","extend":"null"}
            if user_name in user_list:
                return {"code":204,"msg":"注册用户名不能重复","extend":"null"}


            return {"code":200,"msg":"hahaha","extend":"null"}

    return MyRequest()


patcher=patch(target='requests.post',side_effect=mock_register)  # 被替换对象/替换对象

patcher.start()  # 启动补丁

response=requests.post(url='http://localhost:90/login/register',data={'username':'zhangsan','password':'e10adc3949ba59abbe56e057f20f883e'})
print(response.status_code)
print(response.json())

patcher.stop()  # 关闭补丁
