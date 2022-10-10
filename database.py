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

    # 数据库的一系列操作
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
