# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   连接数据库.py
@Desc:
@Create: 2020/09/14 0:18
"""
import mysql.connector
from mysql.connector import Error


# 连接MySQL
def create_connection(host_name, user_name, user_pwd):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_pwd
        )
        print("Connection to MySQL DB Successfull")
    except Error as e:
        print(f"The error '{e}' occurred.")
    return conn


con = create_connection("localhost", "root", "")
print(con)
