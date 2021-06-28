# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   人像动漫化.py
@Desc:
@Create: 2021/06/28 11:15
"""
import base64
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='
response = requests.get(host)
if response:
    access_token = response.json()["access_token"]
'''
人像动漫化
'''
request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
# 二进制方式打开需要处理图片文件
f = open('./images/Pic/小宝01.png', 'rb')  # 打开需要处理的图片
img = base64.b64encode(f.read())

params = {"image": img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
print(response)
if response:
    # 保存文件
    f = open('images/Pic/t2.jpg', 'wb')
    img = (response.json()['image'])
    f.write(base64.b64decode(img))
    f.close()
