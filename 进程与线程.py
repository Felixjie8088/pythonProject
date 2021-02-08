# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   进程与线程.py
@Desc:
@Create: 2020/09/19 15:23
"""
import time
import threading
from multiprocessing import Process


def sleep_time():
    time.sleep(5)
    print("sleep_time")


if __name__ == '__main__':
    t = threading.Thread(target=sleep_time, name="sleep_time_thread")
    t.start()
    # p = Process(target=sleep_time)
    # p.start()
