import yaml
import pymysql
import tools
import encryption
class Database:
    def __init__(self):
        # 打开文件
        f = open('config.yml',encoding="utf-8")
        self.file = yaml.safe_load(f)
        # 读取数据库地址
        self.db = pymysql.connect(
            host=self.file['database']['host'],
            user=encryption.descrypt_3des(self.file['database']['user']),
            password=encryption.descrypt_3des(self.file['database']['password']),
            database=self.file['database']['database'],
            charset=self.file['database']['charset'])
        self.cur = self.db.cursor()

    def use_database(self,data,table,col,time1,time2):
        if data:
            try:
                self.database_save(data, table, col, time1, time2)
                tools.logger.info('数据插入成功%s,%s,%s' % (table, time1, time2))
            except Exception as reason:
                tools.logger.error('数据插入失败%s,%s,%s,%s' % (table, time1, time2, reason))
        else:
            tools.logger.warning('没有数据%s,%s,%s' % (table, time1, time2))

    # 插入所有数据入数据库的一系列操作
    def database_save(self,data,table,col,time1,time2):
        # 查找请求时间段内是否已经有数据了
        sel_result = self.database_select(table,col,time1,time2)
        # 若原有数据库有数据则删除再添加，没有数据直接添加
        if sel_result:
            # 删除当前时间范围的所有数据
            self.database_delete(table,col,time1,time2)
            # 插入当前时间范围内的所有数据
            self.database_insert(data,table)
        else:
            # 插入当前时间范围内的所有数据
            self.database_insert(data,table)


    # 数据库查询操作，基于开始与结束时间
    def database_select(self,table,col,time1,time2):
        sel_sql = "select * from %s where %s between '%s' and '%s'"%(table,col,time1,time2)
        # 检查是否断开连接，断开连接则重新连接
        self.db.ping(reconnect=True)
        # 执行sql语句
        self.cur.execute(sel_sql)
        # 获取查询结果
        sel_result = self.cur.fetchall()
        # 返回查询结果
        return sel_result

    # 数据库删除操作
    def database_delete(self,table,col,time1,time2):
        del_sql = "delete from %s where %s between '%s' and '%s'"%(table,col,time1,time2)
        self.db.ping(reconnect=True)
        self.cur.execute(del_sql)
        self.db.commit()  # 提交到数据库

    # 数据库插入操作
    def database_insert(self,data,table):
        # desc = self.cur.description
        # 迭代数据
        for _data in data:
            ins_sql = "insert into {} values({})".format(
                table,
                ','.join(["'%s'"%str(v) if v!=None else "NULL" for k,v in _data.items()])
            )
            self.db.ping(reconnect=True)
            self.cur.execute(ins_sql)
            self.db.commit()

    # 站点更新动态表
    def count_station_num(self,data,table):
        for _data in data:
            station = _data['WorkCenterCode']
            # 查询表中是否有站点名称，没有添加名称
            sel_sql = "select * from %s where WorkCenterCode = '%s'"%(table,station)
            self.db.ping(reconnect=True)
            # 执行sql语句
            self.cur.execute(sel_sql)
            # 获取查询结果
            sel_result = self.cur.fetchall()
            # 返回查询结果
            if not sel_result:
                ins_sql = "insert into %s values('%s',0)"%(table,station)
                self.db.ping(reconnect=True)
                self.cur.execute(ins_sql)
                self.db.commit()  # 提交到数据库
            else:
                # 有站点名称则直接更新
                update_sql = "update %s set count=count+'1' where WorkCenterCode = '%s'"%(table,station)
                self.db.ping(reconnect=True)
                self.cur.execute(update_sql)
                self.db.commit()  # 提交到数据库

    # 插入站点节拍
    def ins_station_ct(self,table1,table2,col_time,time1,time2):
        # sel time1 和 time2之间的数据
        station_info = list(self.database_select(table1,col_time,time1,time2))
        data = []
        # 遍历每个数据，对每个数据找出最上面一个值
        for _s in station_info:
            _s = list(_s)
            _ModelCode = _s[2]
            _centerCode = _s[5]
            _dateTime = _s[7]
            sel_sql = "select ModelCode,WorkCenterCode,DateTimeScan \
                        from produce_table where WorkCenterCode='%s' and DateTimeScan\
                         <'%s' order by DateTimeScan desc limit 1"%(_centerCode,_dateTime)
            self.db.ping(reconnect=True)
            self.cur.execute(sel_sql)
            sel_result = self.cur.fetchall()
            _dateTime2 = list(sel_result)[0][2]
            # 两个时间相减
            dis = _dateTime - _dateTime2
            _ct = dis.days*24*3600 + dis.seconds
            dict = {
                'ModelCode':_ModelCode,
                'centerCode':_centerCode,
                'DateTime':_dateTime,
                'CycleTime': _ct,
            }
            data.append(dict)
        self.use_database(data,'station_ct_info','DateTimeScan',time1,time2)