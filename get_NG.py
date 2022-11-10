from get_data import GetData
import time
class Get_NG(GetData):
    def __init__(self):
        GetData.__init__(self)
        # 读取URL
        self.url = self.file['get_NG_url']
        # 读取参数
        self.data = self.file['get_NG_data']
        # 请求的间隔时间
        self.request_ct = self.file['get_NG_request_ct']
        # 入参的间隔时间
        self.time_ct = self.file['get_NG_time_ct']
        # 统计表名称
        self.table = self.file['get_NG_table']
        # 时间查询索引名称
        self.col = self.file['get_NG_time_col']

    def run(self):
        count = 0
        while True:
            count += 1
            # 更新入参数据,时间
            time1, time2 = self.update_params(count)
            # 发送请求
            result = self.send_request2(time1, time2)
            # 解析,更新存入数据
            data = self.parse(result)['Data']
            data[0]['start_time'] = time1
            data[0]['end_time'] = time2
            # 存入数据库
            self.database.use_database(data, self.table, self.col, time1, time2)
            # 保持循环
            time.sleep(self.request_ct)

    def update_params(self,count):
        time1, time2 = self.update_time(count, self.time_ct)
        self.data['START_TIME'] = str(time1)
        self.data['END_TIME'] = str(time2)
        return time1,time2