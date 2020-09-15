# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   函数.py
@Desc:
@Create: 2020/08/25 21:40
"""


class SuperMan:
    '''
    A class of superman
    '''

    def __init__(self, name):
        self.name = name
        self.gender = 1
        self.single = False
        self.illness = False

    def nine_negative_kungfu(self):
        return "Ya!"


guojing = SuperMan('guojing')
print(guojing.name)
print(guojing.gender)
kungfu = guojing.nine_negative_kungfu()
print(kungfu)
