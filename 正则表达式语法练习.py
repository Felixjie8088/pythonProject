# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  正则表达式语法练习.py
@Desc:
@Create: 2021/2/26 9:53
"""
import re


# 1.验证手机号码：手机号码的规则是以1开头，第二位可以是345789.后面那9位就可以随意了
# phone_num = '19258951234'
# result = re.match('1[345789]\d{9}',phone_num)
# print(result)
# 2.验证邮箱：邮箱的规则是邮箱名称是用数字、英文字符、下划线组成的，然后是@符号，后面就是域名了
# email = '19258951234@qq.com'
# result = re.match('\w+@[a-z0-9]+\.[a-z]+',email)
# print(result)
# 3.验证URL：URL的规则是前面是HTTP或者HTTPS或者是FTP然后加上一个冒号，再加上一个斜杠，在后面就是可以出现任意非空白字符了
# url = 'https://www.runoob.com/regexp/regexp-syntax.html'
# result = re.match('(http|https|ftp)://\S+',url)
# print(result)
# 4.验证身份证：身份证的规则是总共有18位，前面17位都是数字，后面一位可以是数字也可以是x或者X
id_card = '321322199712230420'
result = re.match('\d{17}(x|X|\d)',id_card)
# result = re.match('\d{17}[\dxX]',id_card)
print(result)