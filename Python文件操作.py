# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Python文件操作.py
@Desc:
@Create: 2021/01/31 17:43
"""

import os

# 打开文件
with open('./File/filetext.txt', encoding='utf-8') as ofile:
    f_readLines = ofile.readlines()
    # 执行完之后需要将读写位置重新定位到开头
    ofile.seek(0)
    f_read = ofile.read()
    print(f_read)
    print(f_readLines)
