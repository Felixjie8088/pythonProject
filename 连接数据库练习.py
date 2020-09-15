# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   连接数据库练习.py
@Desc:
@Create: 2020/09/15 9:43
"""
import mysql.connector
import pymysql
from mysql.connector import Error


def create_connection(host, user, pwd, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db_name
        )
        # conn = pymysql.connect(
        #     host=host,
        #     user=user,
        #     passwd=pwd
        # )

        print("lian jie cheng gong")
    except Error as e:
        print(f'Error is {e}')

    return conn


connection = create_connection('localhost', 'root', '978023zy.*', 'Felix')
print(connection)


# 创建数据库
def create_database(connect, sql_query):
    cursor = connect.cursor()
    try:
        cursor.execute(sql_query)
        print("Database create successfull")
    except Error as e:
        print(f"Error is {e}")


# create_database_query = "CREATE DATABASE Felix"
# create_database(connection, create_database_query)

# 执行对数据库的写入操作-sql
def DBWrite(connect, sql_query):
    cursor = connect.cursor()
    try:
        cursor.execute(sql_query)
        connect.commit()
        print("sql_query execute successfull")
    except Error as e:
        print(f"Error is {e}")


# 执行对数据库的读操作-sql
def DBRead(connect, sql_query):
    cursor = connect.cursor()
    result = None
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
        print("sql_query execute successfull")
    except Error as e:
        print(f"Error is {e}")


# 创建表
create_table_query = """
CREATE TABLE IF NOT EXISTS SYS_User(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    UserName TEXT ,
    Age INT,
    Gendar TEXT
)
"""
# DBWrite(connection, create_table_query)

# 插入数据
insert_data_query = """
INSERT INTO 
`SYS_User`(
    `UserName`,
    `Age`,
    `Gendar`
)
VALUES
('linda',18,'FeMale'),
('杰恩斯',20,'Male'),
('zhangsan',30,'Male')
"""
# DBWrite(connection, insert_data_query)

# 查询数据
read_table_query = """
SELECT * FROM SYS_User
"""
Users = DBRead(connection, read_table_query)
for user in Users:
    print(user)
