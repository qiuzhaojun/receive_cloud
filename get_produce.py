from get_data import GetData
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
        # self.station_count = self.file['****']
        # 时间查询索引名称
        self.col = self.file['get_produce_time_col']

    def run(self):
        count = 0
        while True:
            count += 1
            # 更新入参数据,时间
            time1, time2 = self.update_time(count, self.time_ct)
            self.data['startTime'] = str(time1)
            self.data['endTime'] = str(time2)
            # 发送请求
            result = self.send_request2(time1,time2)
            # 解析
            data = self.parse(result)['Data']
            # 存入数据库
            self.use_database(data,time1,time2)
            # 站点计数
            # self.station_count_num(data)
            # 统计站点工时


    def station_count_num(self,data):
        station = data['s***']
        update_sql = "update %s set count=count+'1' where station = %s"%(self.table,station)
        self.db.ping(reconnect=True)
        self.cur.execute(update_sql)
        self.db.commit()  # 提交到数据库

    def count_station_CT(self,data):
        station = data['****']
        now_time = data['****']
        # 查询站点最近一次的记录时间
        sel_sql = "select * from %s where station=%s and time "


