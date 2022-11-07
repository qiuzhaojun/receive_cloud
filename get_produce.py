from get_data import GetData
# ��ȡ���Ͻӿ���
class GetProduce(GetData):
    def __init__(self):
        GetData.__init__(self)
        # ��ȡURL
        self.url = self.file['get_produce_url']
        # ��ȡ����
        self.data = self.file['get_produce_data']
        # ����ļ��ʱ��
        self.request_ct = self.file['get_produce_request_ct']
        # ��εļ��ʱ��
        self.time_ct = self.file['get_produce_time_cr']
        # ��������ͳ�Ʊ�����
        self.table = self.file['get_produce_table']
        # վ�����������
        # self.station_count = self.file['****']
        # ʱ���ѯ��������
        self.col = self.file['get_produce_time_col']

    def run(self):
        count = 0
        while True:
            count += 1
            # �����������,ʱ��
            time1, time2 = self.update_time(count, self.time_ct)
            self.data['startTime'] = str(time1)
            self.data['endTime'] = str(time2)
            # ��������
            result = self.send_request2(time1,time2)
            # ����
            data = self.parse(result)['Data']
            # �������ݿ�
            self.use_database(data,time1,time2)
            # վ�����
            # self.station_count_num(data)
            # ͳ��վ�㹤ʱ


    def station_count_num(self,data):
        station = data['s***']
        update_sql = "update %s set count=count+'1' where station = %s"%(self.table,station)
        self.db.ping(reconnect=True)
        self.cur.execute(update_sql)
        self.db.commit()  # �ύ�����ݿ�

    def count_station_CT(self,data):
        station = data['****']
        now_time = data['****']
        # ��ѯվ�����һ�εļ�¼ʱ��
        sel_sql = "select * from %s where station=%s and time "


