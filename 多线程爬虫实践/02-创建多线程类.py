# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   02-创建多线程类.py
@Desc:
@Create: 2021/03/04 22:06
"""
import time
import threading

class Coding(threading.Thread):
    def run(self) -> None:
        this_thread = threading.current_thread()
        print(this_thread.name)
        for x in range(3):
            print('第{}次写代码'.format(x))
            time.sleep(1)

class Drawing(threading.Thread):
    def run(self) -> None:
        this_thread = threading.current_thread()
        print(this_thread.name)
        for x in range(3):
            print('第{}次画图'.format(x))
            time.sleep(1)

def multi_thread():
    thread_coding = Coding()
    thread_drawing = Drawing()

    thread_coding.start()
    thread_drawing.start()


if __name__ == '__main__':
    multi_thread()

# def coding():
#     this_thread = threading.current_thread()
#     print(this_thread.name)
#     for x in range(3):
#         print('第{}次写代码'.format(x))
#         time.sleep(1)
#
#
# def drawing():
#     this_thread = threading.current_thread()
#     print(this_thread.name)
#     for x in range(3):
#         print('第{}次画图'.format(x))
#         time.sleep(1)
#
#
# """
# 多线程
# """
#
#
# def multi_thread():
#     thread_coding = threading.Thread(target=coding, name='coding')
#     thread_drawing = threading.Thread(target=drawing, name='drawing')
#
#     thread_coding.start()
#     thread_drawing.start()
#
#
# if __name__ == '__main__':
#     # single_thread()
#     multi_thread()
