import logging.handlers
import json
import datetime
# 全局变量token存储
token_str = ''
mToken_str = ''
# 创建一个logger实例并设置日志级别
logger = logging.getLogger('alg_name')
logger.setLevel(logging.DEBUG)
# 配置handler，拟将日志记录输出至/log/文件夹
file_name = './log_temp/alg_name_log.log'  # 注意：如果/log/文件夹不存在，则需要新建
# 每天午夜生成alg_name_log.log文件，最多保留30天
file_handler = logging.handlers.TimedRotatingFileHandler(file_name, when='MIDNIGHT', interval=1,backupCount=30)
# 配置handler，拟将日志记录输出在控制台
stdout_handler = logging.StreamHandler()
# 配置formatter
formatter = logging.Formatter('%(levelname)s - %(asctime)s [%(filename)s:%(lineno)d] %(message)s \n')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
# 添加handler至logger
logger.addHandler(file_handler)
# 添加handler至logger
logger.addHandler(stdout_handler)
# # 下面的内容都是写在算法文件里你需要的地方
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')




