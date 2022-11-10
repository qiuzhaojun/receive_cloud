from get_data import GetData
import time
class GetCT(GetData):
    def __init__(self):
        GetData.__init__(self)
        # 读取get参数间隔
        self.time_ct = self.file['get_ct_time_ct']
        # 读取获取频率
        self.request_ct = self.file['get_ct_request_ct']
    def run(self):
        count = 0
        while True:
            count += 1
            # 1 获取时间time1,time2
            time1,time2 = self.update_time(count,self.time_ct)
            # 2 sel time1 和 time2之间的数据
            self.database.ins_station_ct('produce_table','station_ct_info','DateTimeScan',time1,time2)
            # 保持循环
            time.sleep(self.request_ct)


if __name__ == '__main__':
    get1 = GetCT()
    get1.run()