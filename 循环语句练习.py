# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   循环语句练习.py
@Desc:   执行语句 pyinstaller --onefile 循环语句练习.py
@Create: 2020/08/21 11:24
"""
import random
import os

# 生成随机数
random_number = random.randint(1, 100)
# 无限循环
while True:
    number_input = input('请输入一个0-100之间的数字：')
    # 判断输入的是否为数字
    if not number_input.isdigit():
        print('请输入数字！')
    elif int(number_input) < 0 or int(number_input) > 100:
        print('你所输入的超出范围！')
    else:
        if int(number_input) == random_number:
            print('ok')
            break
        elif int(number_input) < random_number:
            print('小了')
        else:
            print('大了')

os.system('pause')
