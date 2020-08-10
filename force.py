# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   force.py
@Desc:   Math练习
@Create: 2020/08/10 14:50
"""
import math

f1 = 20
f2 = 10
alpha = math.pi / 3
# 正弦函数
x_force = f1 + f2 * math.sin(alpha)
# 余弦函数
y_force = f2 * math.cos(alpha)
# 平方根函数
force = math.sqrt(x_force * x_force + y_force ** 2)

print('The result is:', round(force, 2), 'N')
