import MySQLdb
import DataManipulation as dm


# 创建SQLDB类
class SQLDB:
    # 创建self函数
    def __init__(self, ip: str, username: str, password: str, sql_name: str):  # 创建链接数据库变量
        self.ip = ip  # SQL数据库IP地址
        self.username = username  # 数据库的用户名
        self.password = password  # 数据库密码
        self.sql_name = sql_name  # 数据库名称

    # 创建数据库表
    def crateSql(self, form_name: str, sql_lang: str):
        # 创建数据库连接
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 如果数据表已经存在使用 execute() 方法删除表。
        cursor.execute("DROP TABLE IF EXISTS %s" % form_name)
        try:
            # 创建数据表SQL语句
            cursor.execute(sql_lang)
            # 关闭数据库连接
            db.close()
            return "Yes"
        except MySQLdb.Error:
            db.close()
            return "Error"

    # 插入数据
    def insertSql(self, sql):
        # 连接到数据库
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        # 获取操作游标
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            # 关闭数据库连接
            db.close()
            # 返回yes
            return 'Yes'
        except MySQLdb.Error:
            # 如果报错则进行回滚
            db.rollback()
            # 关闭数据库连接
            db.close()
            # 返回error
            return 'Error'

    # 清空数据
    def clearSql(self, form):
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        cursor = db.cursor()
        sql = 'truncate table %s' % form
        try:
            cursor.execute(sql)
            db.close()
            return "Yes"
        except MySQLdb.Error:
            db.close()
            return "Error"

    # 删除数据
    def deleteSql(self, sql):
        # 连接到数据库
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        # 获取操作游标
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
            db.close()
            return "Yes"
        except MySQLdb.Error:
            db.close()
            return "Error"

    # 查询数据
    def searchSql(self, sql):
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        # 获取操作游标
        cursor = db.cursor()
        # 定义返回值
        l1 = []
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for i in results:
                l2 = []
                for j in i:
                    l2.append(j)
                l1.append(l2)
            if l1 is None:
                return []
            else:
                return l1
        except MySQLdb.Error:
            db.close()
            return "Error"

    # 更新数据
    def updateSql(self, sql):
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        cursor = db.cursor()
        # SQL 更新语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            db.close()
            return "Yes"
        except MySQLdb.Error:
            # 发生错误时回滚
            db.rollback()
            # 关闭数据库连接
            db.close()
            return "Error"

    # 获取所有数据
    def allSql(self, form):
        db = MySQLdb.connect(self.ip, self.username, self.password, self.sql_name)
        cursor = db.cursor()
        sql = "SELECT * FROM %s" % form
        try:
            cursor.execute(sql)
            mydata = cursor.fetchall()  # 获取全部数据
            l1 = []
            l2 = []
            if len(mydata) == 0:
                return "Error"
            else:
                for data in mydata:
                    l1.append(data)
                db.close()
                for i in l1:
                    l3 = []
                    for j in i:
                        l3.append(j)
                    l2.append(l3)
                return l2
        except MySQLdb.Error:
            dm.Logging.errorLog("查询数据失败")
