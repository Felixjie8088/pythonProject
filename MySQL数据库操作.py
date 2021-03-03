# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   MySQL数据库操作.py
@Desc:
@Create: 2021/03/03 21:52
"""
import pymysql

'''
MySQL数据库连接、查询操作
'''
# 使用pymysql.connect连接数据库
db = pymysql.connect(host='localhost', port=3306, user='root', password='Felix', database='test', charset='utf8')


def search_db(db):
    # 使用cursor对象操作数据库
    cursor = db.cursor()
    # 使用cursor.execute方法执行SQL语句
    cursor.execute("select * from article")
    # 使用cursor.fetchone()方法查询结果集中的一条数据
    result = cursor.fetchmany(10)
    print(result)


'''
MySQL数据插入操作
'''


def insert_db(db):
    # 使用cursor对象操作数据库
    cursor = db.cursor()
    # 插入SQL
    sql_insert = """
    insert article(title,content)
    values('b','12321')
    """
    # 调用cursor.execute方法执行SQL语句
    cursor.execute(sql_insert)
    # 提交操作
    db.commit()
    # 关闭数据库连接
    db.close()


'''
MySQL数据删除操作
'''


def delete_db(db):
    # 使用cursor对象操作数据库
    cursor = db.cursor()
    # 插入SQL
    sql_delete = """
    delete from article where title = 'b'
    """
    # 调用cursor.execute方法执行SQL语句
    cursor.execute(sql_delete)
    # 提交操作
    db.commit()
    # 关闭数据库连接
    db.close()


'''
MySQL数据更新操作
'''


def update_db(db):
    # 使用cursor对象操作数据库
    cursor = db.cursor()
    # 插入SQL
    sql_update = """
    update article set content = '你好呀！' where title = 'a'
    """
    # 调用cursor.execute方法执行SQL语句
    cursor.execute(sql_update)
    # 提交操作
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    search_db(db)
    update_db(db)
