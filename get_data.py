import datetime
import json
import time
import requests
import yaml

import tools
import database

class GetData:
    def __init__(self):
        # 打开文件
        f = open('config.yml',encoding="utf-8")
        self.file = yaml.safe_load(f)
        # 读取请求头
        self.headers = self.file['headers']
        # 初始化数据库操作类
        self.database = database.Database()
        # 加载预设置时间
        self.debug_time = self.file['debug_time']
        self.setting_time = self.file['setting_time']
        # 请求接口失败后频率
        self.get_data_request_fail_ct = self.file['get_data_request_fail_ct']
        # 预定义
        self.time_ct = None
        self.table = None
        self.data = None
        self.url = None
        self.col = None

    # 更新参数
    def update_params(self,count):
        time1, time2 = self.update_time(count, self.time_ct)
        self.data['params']['p02'] = str(time1)
        self.data['params']['p03'] = str(time2)
        return time1,time2

    # 更新参数时间
    def update_time(self,count,time_ct):
        # 使用固定时间 + 间隔时间*循环次数
        if self.debug_time:
            init_time_str = str(self.setting_time)
            init_time = datetime.datetime.strptime(init_time_str, "%Y-%m-%d %H:%M:%S")
            time1 = init_time + datetime.timedelta(hours=1 * (count - 1))
            time2 = time1 + datetime.timedelta(hours=1)
        # 使用系统时间 + 间隔时间
        else:
            now = datetime.datetime.now() # 当前系统时间
            pre = now - datetime.timedelta(seconds=time_ct) # 当前系统时间+间隔时间
            time1 = pre.strftime("%Y-%m-%d %H:%M:%S")
            time2 = now.strftime("%Y-%m-%d %H:%M:%S")
        return time1, time2

    # 发送请求
    def send_request(self,time1,time2):
        while True:
            try:
                # 更新参数需要在请求前
                self.headers['token'] = tools.token_str
                result = requests.post(url=self.url, headers=self.headers, json=self.data)
                if result.status_code == 200:
                    # 成功信息参数
                    msg = self.parse(result)['msg']
                    tools.logger.info('请求成功 %s,%s,%s,%s' % (msg, self.table, time1, time2))
                    break
                else:
                    tools.logger.error('请求失败，重新请求 %s,%s,%s,%s' % (self.table, time1, time2, result.text))
            except Exception as reason:
                tools.logger.error('请求过程出现异常 %s,%s,%s,%s' % (self.table, time1, time2, reason))
            time.sleep(self.get_data_request_fail_ct)
        return result

    # 发送请求2
    def send_request2(self,time1,time2):
        while True:
            try:
                # 更新参数需要在请求前
                self.headers['Authorization'] = tools.mToken_str
                result = requests.post(url=self.url, headers=self.headers, json=self.data)
                if result.status_code == 200:
                    # 成功信息参数
                    msg = self.parse(result)['Message']
                    tools.logger.info('请求成功 %s,%s,%s,%s' % (msg, self.table, time1, time2))
                    break
                else:
                    tools.logger.error('请求失败，重新请求 %s,%s,%s,%s' % (self.table, time1, time2, result.text))
            except Exception as reason:
                tools.logger.error('请求过程出现异常 %s,%s,%s,%s' % (self.table, time1, time2, reason))
            time.sleep(self.get_data_request_fail_ct)
        return result

    # 解析
    def parse(self,result):
        result_bytes = result.content  # 返回字节串
        result_str = result_bytes.decode()  # 返回字符串
        result_json = json.loads(result_str)  # 字符串转化为json格式
        return result_json

    # 数据库操作
    def use_database(self,data,time1,time2):
        if data:
            try:
                self.database.database_save(data, self.table, self.col, time1, time2)
                tools.logger.info('数据插入成功%s,%s,%s' % (self.table, time1, time2))
            except Exception as reason:
                tools.logger.error('数据插入失败%s,%s,%s,%s' % (self.table, time1, time2, reason))
        else:
            tools.logger.warning('没有数据%s,%s,%s' % (self.table, time1, time2))







