# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   03-多线程全局变量.py
@Desc:
@Create: 2021/03/04 22:21
"""
import threading

value = 0
# 使用锁的原则
# 1.把尽量少的和不耗时的代码放到锁中执行
# 2.代码执行完之后要记得释放锁
glock = threading.Lock()

def add_value():
    global value
    # 加锁
    glock.acquire()
    for i in range(100000000):
        value += 1
    # 释放锁
    glock.release()
    print('value的值是%d', value)


def run_test():
    for i in range(2):
        th = threading.Thread(target=add_value(), name='add_value')

        th.start()


if __name__ == '__main__':
    run_test()
