# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   练习2（填写数字转英文单词）.py
@Desc:
@Create: 2020/08/12 17:18
"""
num_input = input('请输入数字：')

lst_en_num = dict({'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', })

str_output = []

for n in num_input:
    str_output.append(lst_en_num.get(n))

print('转换后的英文是：', ' '.join(str_output))
