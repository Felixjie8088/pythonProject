# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   处理异常.py
@Desc:
@Create: 2020/09/13 21:49
"""
while True:
    try:
        a = float(input('first number:'))
        b = float(input('second number:'))
        str_eval = input('zhixingdebiaodashi:')
        r = eval(str_eval)
        print("{0}/{1}={2}".format(a, b, r))
        break
    except ZeroDivisionError:
        print('Zero can not by division.Try again!')
    except ValueError:
        print('Please enter number.Try again!')
    except:
        break
