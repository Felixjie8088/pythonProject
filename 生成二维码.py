# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   生成二维码.py
@Desc:
@Create: 2021/02/08 23:00
"""

from MyQR import myqr

myqr.run(
    words='hello,xioabao',
    colorized=True,
    picture='./images/Pic/gif-01.gif',
    save_name='xiaobao.gif',
    save_dir='./images/Pic/'
)