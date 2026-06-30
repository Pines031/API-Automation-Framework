import logging
from configs.config import config
from datetime import datetime

"""
日志对于测试的意义：
1.测试过程可追溯,保存测试历史，便于追溯和分析
2.提供问题定位与调试方向
"""

time=datetime.now().strftime('%Y%m%d')  # 获取当前日期
logname=f'{time}.log'

class Logger:

    def __init__(self,name):

        log_path=config.LOG_PATH
        log_path.mkdir(parents=True,exist_ok=True)

        self.logger=logging.getLogger(name=name) # 创建一个logging.Logger实例,使用logging.getLogger()获取或创建一个指定名称的日志记录器
        self.logger.setLevel(logging.INFO) # 设置日志记录器的级别为INFO

        # 检查这个记录器是否已经配置了处理器（handlers），避免重复添加处理器，导致日志重复输出
        if not self.logger.handlers:
            formatter=logging.Formatter( # 创建一个日志格式化器（Formatter）,定义日志的输出格式：级别 时间 名称 消息
                "%(levelname)s %(asctime)s %(name)s %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            fh=logging.FileHandler(config.LOG_PATH/logname,encoding='utf-8') # 创建一个文件处理器,将日志写入到文件中
            fh.setFormatter(formatter) # 将前面创建的格式化器设置给文件处理器

            self.logger.addHandler(fh) # 将文件处理器添加到日志记录器中

    def getlogger(self):
        return self.logger


if __name__ == '__main__':
    logger1 = Logger('test').getlogger()
    logger1.info('cs')
