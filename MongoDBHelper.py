# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   MongoDBHelper.py
@Desc:
@Create: 2020/09/24 15:19
"""
# 数据库连接相关
from pymongo import MongoClient
# 时间
from datetime import datetime

"""
ObjectId 是一个12字节 BSON 类型数据，有以下格式：

前4个字节表示时间戳
接下来的3个字节是机器标识码
紧接的两个字节由进程id组成（PID）
最后三个字节是随机数。
MongoDB中存储的文档必须有一个"_id"键。这个键的值可以是任何类型的，默认是个ObjectId对象。
在一个集合里面，每个文档都有唯一的"_id"值，来确保集合里面每个文档都能被唯一标识。
MongoDB采用ObjectId，而不是其他比较常规的做法（比如自动增加的主键）的主要原因，因为在多个 服务器上同步自动增加主键值既费力还费时。
"""
from bson.objectid import ObjectId


class MongoDataBase:
    def __new__(cls, *args, **kwargs):
        '''单例模式'''
        if not hasattr(cls, "instance"):
            cls.instance = super(MongoDataBase, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        '''连接数据库'''
        self.client = MongoClient()
        self.db = self.client['Mongo-Felix-Test01']

    def add_one_data(self):
        '''添加一条数据'''
        add_data = {
            "author": "Felix",
            "text": "1243231",
            "createtime": datetime.utcnow()
        }
        return self.db.author.insert_one(add_data)

    def get_one_data(self):
        '''查询一条数据'''
        return self.db.author.find_one()