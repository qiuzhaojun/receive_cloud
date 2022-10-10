from get_data import GetData
import time
# 获取RFID接口类
class GetRfid(GetData):
    def __init__(self):
        GetData.__init__(self)
        # 读取URL
        self.url = self.file['get_rfid_url']
        # 读取参数
        self.data = self.file['get_rfid_data']
        # 读取请求头
        self.headers = self.file['headers']
        # 请求的间隔时间
        self.request_ct = self.file['get_rfid_request_ct']
        # 入参的间隔时间
        self.time_ct = self.file['get_rfid_time_cr']
        # 表名称
        self.table = self.file['get_rfid_table']
        # 时间查询索引名称
        self.col = self.file['get_rfid_time_col']

    def run(self):
        count = 0
        while True:
            count += 1
            # 更新入参数据,时间
            time1,time2 = self.update_params(count)
            # 发送请求
            result = self.send_request(time1,time2)
            # 解析
            data = self.parse(result)['data']
            # 存入数据库
            self.use_database(data,time1,time2)
            # 保持循环
            time.sleep(self.request_ct)