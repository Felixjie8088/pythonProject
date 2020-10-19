# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   02-urlencode.py
@Desc:
@Create: 2020/10/19 15:39
"""
from urllib import parse

data = {'name': '爬虫基础', 'greet': 'hello world', 'age': 100}
# 将字典数据进行编码成字符串
encodeData = parse.urlencode(data)
# 将编码后的字符串进行解码
decodeData = parse.unquote(encodeData)
print(encodeData)
print(decodeData)
