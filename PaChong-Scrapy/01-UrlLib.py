# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   01-UrlLib.py
@Desc:
@Create: 2020/10/19 14:47
"""
from urllib import request

request.urlretrieve("https://bkimg.cdn.bcebos.com/pic/cb8065380cd79123b9bc93cba7345982b2b78034?x-bce-process=image/watermark,image_d2F0ZXIvYmFpa2UxMTY=,g_7,xp_5,yp_5", "../images/AIFaceImg/shiyuanlimei.jpg")

# resp = request.urlopen("http://192.168.1.35:8000/Login.html")
#
# print(resp.read())
