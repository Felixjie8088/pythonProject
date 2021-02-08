# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   url解析.py
@Desc:
@Create: 2021/01/31 19:26
"""
from urllib import parse

url = 'https://www.baidu.com/index.html;user?id=S#comment'

# result = parse.urlparse(url)
result = parse.urlsplit(url)

print(result)
print(result.scheme)
'''
urlparse中有params属性
urlsplit中没有params属性
'''