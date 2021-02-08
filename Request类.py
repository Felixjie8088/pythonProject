# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Request类.py
@Desc:
@Create: 2021/01/31 19:32
"""
from urllib import request

url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
}
rq = request.Request(url, headers=headers)
resopnse = request.urlopen(rq)
print(resopnse.read())
