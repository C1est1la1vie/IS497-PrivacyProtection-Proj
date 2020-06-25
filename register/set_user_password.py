import pymysql
import datetime
import hashlib
# 打开数据库连接
def mysql_insert_data(password_get,sno_get):
    db = pymysql.connect("39.101.187.212", "root", "12345678", "clients", charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    sno = password_get
    password = sno_get
    c_time = datetime.datetime.now()
    m=hashlib.md5()
    m.update(password.encode('utf-8'))
    password_hash = m.hexdigest()
    sql = "INSERT INTO user (sno, password,c_time) VALUES (%s, %s , %s)"
    val = (sno, password_hash,c_time)
    cursor.execute(sql, val)
    db.commit()
    # 关闭数据库连接
    db.close()

if __name__=="__main__":
    sno = "517021910855"
    password = "test123"
    mysql_insert_data(sno,password)