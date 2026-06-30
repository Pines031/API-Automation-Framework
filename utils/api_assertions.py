from logs.mylog import Logger

logger = Logger('TESTCASE').getlogger()


class Assertions:

	@staticmethod
	def assert_jsondata(jsondata: dict, key: str, expect_value: any):
		"""json断言"""
		methodname = Assertions.assert_jsondata.__name__  # 获取当前方法的名称
		try:
			actual_value = jsondata.get(key)  # 实际值，字典查询
			assert actual_value == expect_value, \
				f'实际结果{actual_value} 预期结果{expect_value}'  # 断言，定义异常信息
			logger.info(f'{methodname}断言通过')
		except AssertionError as e:
			logger.error(f'{methodname}断言失败：{e}')
			raise e
		except Exception as e:
			logger.error(f'{methodname}用例执行异常：{e}')
			raise e
		finally:
			logger.info('=' * 80)

	@staticmethod
	def assert_code(actual_code: int, expect_code: int):
		"""httpcode断言"""
		methodname = Assertions.assert_code.__name__
		try:
			assert actual_code == expect_code, \
				f'实际结果{actual_code} 预期结果{expect_code}'
			logger.info(f'{methodname}断言通过')
		except AssertionError as e:
			logger.error(f'{methodname}断言失败：{e}')
			raise e
		except Exception as e:
			logger.error(f'{methodname}用例执行异常：{e}')
			raise e
		finally:
			logger.info('=' * 80)

	@staticmethod
	def assert_jsondata_many(jsondata: dict, keylist: list, expect_value: any):
		"""json断言-嵌套对象"""
		methodname = Assertions.assert_jsondata_many.__name__
		actual_value = jsondata
		try:
			for i in range(len(keylist)):
				actual_value = actual_value.get(keylist[i])
			assert actual_value == expect_value, \
				f'实际结果{actual_value} 预期结果{expect_value}'
			logger.info(f'{methodname}断言通过')
		except AssertionError as e:
			logger.error(f'{methodname}断言失败：{e}')
			raise e
		except Exception as e:
			logger.error(f'{methodname}用例执行异常：{e}')
			raise e
		finally:
			logger.info('=' * 80)

	@staticmethod
	def assert_data_in(expect_values:any,data:any):
		"""断言匹配，是否包含特定数据"""
		methodname = Assertions.assert_data_in.__name__
		try:
			assert expect_values in data,\
			f'{methodname} 未匹配到数据{expect_values}'
			logger.info(f'{methodname}断言通过')
		except AssertionError as e:
			logger.error(f'{methodname}断言失败：{e}')
			raise e
		except Exception as e:
			logger.error(f'{methodname}用例执行异常：{e}')
			raise e
		finally:
			logger.info('=' * 80)


assertions=Assertions()

if __name__ == '__main__':
	test_json={
		"name":"lisi",
		"msg":{
			"age":18,
			"is":1
		}
	}
	assertions.assert_jsondata_many(test_json,['msg','age'],20)