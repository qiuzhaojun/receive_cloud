from get_data import GetData
import time
# 获取物料接口类
class GetProduce(GetData):
    def __init__(self):
        GetData.__init__(self)
        # 读取URL
        self.url = self.file['get_produce_url']
        # 读取参数
        self.data = self.file['get_produce_data']
        # 请求的间隔时间
        self.request_ct = self.file['get_produce_request_ct']
        # 入参的间隔时间
        self.time_ct = self.file['get_produce_time_cr']
        # 生产过程统计表名称
        self.table = self.file['get_produce_table']
        # 站点计数表名称
        self.station_status_info = self.file['station_status_info']
        # 时间查询索引名称
        self.col = self.file['get_produce_time_col']

    def run(self):
        count = 0
        while True:
            count += 1
            # 更新入参数据,时间
            time1, time2 = self.update_params(count)
            # 发送请求
            result = self.send_request2(time1,time2)
            # 解析
            data = self.parse(result)['Data']
            # 存入数据库
            self.database.use_database(data,self.table,self.col,time1,time2)
            # 站点计数
            self.database.count_station_num(data,self.station_status_info)
            # 保持循环
            time.sleep(self.request_ct)

    def update_params(self,count):
        time1, time2 = self.update_time(count, self.time_ct)
        self.data['startTime'] = str(time1)
        self.data['endTime'] = str(time2)
        return time1,time2