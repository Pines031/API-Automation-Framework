import os
from configs.config import config

if __name__ == '__main__':
    # os.system('pytest')
    # os.system('pytest -v -k "test_0627" --html')   # -v 展示明细
    # os.system('pytest -v -k "test_0626"')  # -k 所搜对应命名的测试用例
    os.system(f'pytest -v -k "test_0627"  --html={config.REPORT_PATH}/0626.html')
    # os.system('pytest -v -m "th626"')  # -m 执行对应标记的测试用例


    """
    1.模块的命名，以test_作为开头
    2.函数方法的命名，以test_作为开头
    3.类命名，以Test作为开头
    """