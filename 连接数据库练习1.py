# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   连接数据库练习1.py
@Desc:
@Create: 2020/09/14 22:10
"""
import mysql.connector
import pymysql
from mysql.connector import Error


def connect_mysql(host_name, user_name, user_pwd):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_pwd
        )
        # conn = pymysql.connect(host_name, user_name, user_pwd)
        print("Connect Successfull")
    except Error as e:
        print(f"Error:{e}")
    return conn


print(connect_mysql("localhost", "root", "978023zy.*"))
