# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   文件读写.py
@Desc:
@Create: 2020/09/03 13:57
"""
import os

# r：以读的方式打开文件，默认
# w：以写的方式打开文件，如果文件存在，那么就覆盖文件，否则就新建文件
# a：以写的方式打开文件，如果文件存在，那么就在文件内容的最后增加内容，否则就新建文件
# b：以二进制模式打开文件。不单独使用，配合r、w、a等模式使用
# +：同时实现读写操作。不单独使用，配合r、w、a等模式使用
# x：创建文件，如果存在则无法创建

f = open('./File/filetext.txt', 'w')
f.write("Felix Y")
# 必须要写，不然是不会内容是不会写入文件的
f.close()

fr = open('./File/filetext.txt')
print(fr.read())
fr.close()

with open('./File/filetext.txt', 'a') as f2:
    f2.write('\nJIE')

fr2 = open('./File/filetext.txt')
print(fr2.read())
fr2.close()
