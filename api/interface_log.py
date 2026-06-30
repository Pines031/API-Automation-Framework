import time
import requests
from requests.exceptions import ConnectionError
from logs.mylog import Logger

logger = Logger("INTERFACE").getlogger()


class Interface:

	def __init__(self, base_url):
		self.session = requests.session()  # 会话
		self.base_url = base_url  # 基础url

	def all(self, url, method, **params):
		httpcode = None
		jsondata = None
		complete_url = f'{self.base_url}{url}' # 拼接得到完整的url

		#记录请求数据
		logger.info(f'请求URL:{complete_url}')
		logger.info(f'请求方式:{method.upper()}\n请求参数:{params}')

		try:
			response=self.session.request(url=complete_url,method=method,**params)  # 发送请求
			httpcode=response.status_code  # 获取httpcode
			if 'application/json' in response.headers.get('Content-Type'):
				jsondata = response.json()
				logger.info('HTTPCODE:{}\n响应数据:{}'.format(httpcode, jsondata))  # 记录json响应数据
				# token处理，将登录接口返回的token，维护进会话中
				if jsondata.get('token'):
					token=jsondata.get('token')
					self.session.headers.update({"Authorization":f"Bearer {token}"})
				return {"httpcode": httpcode, "jsondata": jsondata}
			else:
				textdata = response.text
				logger.info('HTTPCODE:{}\n响应数据:{}'.format(httpcode, textdata[:500]))  # 记录text响应数据
				return {"httpcode": httpcode, "jsondata": jsondata, "textdata": textdata}

		except ConnectionError :
			logger.warning('服务连接失败')  # 记录连接失败
			return {"httpcode":httpcode,"jsondata":jsondata}
		except Exception as e:
			logger.error(f'{e.__class__.__name__} : {e}')  # 记录其他异常情况
			return {"httpcode":httpcode,"jsondata":jsondata}

# 下面是便捷方法，return调用all方法
	def get(self, url,  **params):
		return self.all(url=url,method='GET',**params)

	def post(self, url,**params):
		return self.all(url=url,method='POST',**params)

	def delete(self, url, **params):
		return self.all(url=url, method='DELETE',**params)

	def put(self, url,**params):
		return self.all(url=url, method='PUT',**params)


if __name__ == '__main__':
	request=Interface('http://localhost:90')
	request.get(url='/login/verifyLogin',params={'username': 'lisi', 'password': 'e10adc3949ba59abbe56e057f20f883e'})