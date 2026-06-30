import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent  #确认路径


class Config:
    # 接口配置
    TEST_WEBSITE='http://localhost:90'

    # 数据库配置
    LOCAL_DATABASE={
        "host":"localhost",
        "port":3306,
        "user":"root",
        "password":"root"
    }

    # 测试配置
    TEST_DATA_PATH=BASE_DIR/"test_data"
    LOG_PATH=BASE_DIR/"logs"
    REPORT_PATH=BASE_DIR/"test_report"
    TEST_CASE_PATH=BASE_DIR/"test_cases"
    API_PATH=BASE_DIR/"api"
    UTILS_PATH=BASE_DIR/"utils"
    TEST_PATH=BASE_DIR/"stu"

    ALLURE_PATH=REPORT_PATH/'allure-results'


config=Config()  # 创建全局实例

if __name__ == '__main__':
    print(BASE_DIR)
    config.TEST_DATA_PATH.mkdir(parents=True, exist_ok=True)
    config.LOG_PATH.mkdir(parents=True, exist_ok=True)
    config.REPORT_PATH.mkdir(parents=True, exist_ok=True)
    config.TEST_CASE_PATH.mkdir(parents=True, exist_ok=True)
    config.API_PATH.mkdir(parents=True, exist_ok=True)
    config.UTILS_PATH.mkdir(parents=True, exist_ok=True)
    config.TEST_PATH.mkdir(parents=True, exist_ok=True)
    config.ALLURE_PATH.mkdir(parents=True, exist_ok=True)

