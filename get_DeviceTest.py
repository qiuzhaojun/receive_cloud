from get_data import GetData
import time
class Get_DeviceTest(GetData):
    def __init__(self):
        GetData.__init__(self)
        # 读取URL
        self.url = self.file['get_test_url']
        # 读取参数
        self.data = self.file['get_test_data']
        # 请求的间隔时间
        self.request_ct = self.file['get_test_request_ct']
        # 入参的间隔时间
        self.time_ct = self.file['get_test_time_ct']
        # 统计表名称
        self.table = self.file['get_test_table']
        # 时间查询索引名称
        self.col = self.file['get_test_time_col']

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
            self.update_data(data)
            # 存入数据库
            self.database.use_database(data, self.table, self.col, time1, time2)
            # 保持循环
            time.sleep(self.request_ct)

    def update_params(self,count):
        time1, time2 = self.update_time(count, self.time_ct)
        self.data['startTime'] = str(time1)
        self.data['endTime'] = str(time2)
        return time1,time2

    def update_data(self,data):
        for _data in data:
            n = 0
            for _item in _data["TestItemList"]:
                _data['test%svalue'%n] = _item['TestValue']
                _data['test%sStatus'%n] = _item['TestStatus']
                n += 1
            del _data['TestItemList']
            del _data['WipLog']
