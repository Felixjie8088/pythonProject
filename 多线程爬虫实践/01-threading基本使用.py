# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   01-threading基本使用.py
@Desc:
@Create: 2021/03/04 21:51
"""
import time
import threading


def coding():
    for x in range(3):
        print('第{}次写代码'.format(x))
        time.sleep(1)


def drawing():
    for x in range(3):
        print('第{}次画图'.format(x))
        time.sleep(1)


"""
单线程
"""


def single_thread():
    coding()
    drawing()


"""
多线程
"""


def multi_thread():
    thread_coding = threading.Thread(target=coding)
    thread_drawing = threading.Thread(target=drawing)

    thread_coding.start()
    thread_drawing.start()


if __name__ == '__main__':
    # single_thread()
    multi_thread()
