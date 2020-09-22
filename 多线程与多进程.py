# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   多线程与多进程.py
@Desc:
@Create: 2020/09/18 10:57
"""
# 时间
import time
# 线程
import threading
# 进程
from multiprocessing import Process


def sleep_time(timer):
    time.sleep(timer)
    print(f"sleep {timer}")


# 开启一个线程来执行sleep_time方法
thread = threading.Thread(target=sleep_time(5), name="sleep_time thread")
thread.start()

print(__name__)

if __name__ == '__main__':
    # 开启一个进程执行sleep_time方法
    p = Process(target=sleep_time(5))
    p.start()
