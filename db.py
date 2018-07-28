import pymysql
from config import *

# 获取数据库连接
def get_db():
    return pymysql.connect(HOST, USER, PASSWORD, DATABASE)

# 执行查询多条的sql语句
def select(sql):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        db.rollback()
    finally:
        db.close()


# 执行查询单条的sql语句
def select_one(sql):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        db.rollback()
    finally:
        db.close()