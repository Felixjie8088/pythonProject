# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   04-Lock版本生产者和消费者模式.py
@Desc:
@Create: 2021/03/04 22:48
"""
import time
import threading
import random

# 中间容器（全局）
gMoney = 0
gCondition = threading.Condition()
gTimes = 0


# 生产者
class Producer(threading.Thread):
    def run(self) -> None:
        print(threading.current_thread().name)
        while True:
            global gMoney
            global gCondition
            global gTimes
            gCondition.acquire()
            if gTimes >= 10:
                gCondition.release()
                break
            Money = random.randint(0, 100)
            gMoney += Money
            gTimes += 1
            print('%s生产了Money:%d元\n' % (threading.current_thread().name, Money))
            print('现在gMoney是%d元\n' % gMoney)
            time.sleep(0.5)
            gCondition.notify_all()
            gCondition.release()


# 消费者
class Consumer(threading.Thread):
    def run(self) -> None:
        print(threading.current_thread().name)
        while True:
            global gMoney
            global gTimes
            gCondition.acquire()
            Money = random.randint(100, 1000)
            if gMoney >= Money:
                gMoney -= Money
                print('%s消费了Money:%d元\n' % (threading.current_thread().name, Money))
            else:
                if gTimes >= 10:
                    glock.release()
                    break
                print('%s想要消费Money:%d元，但是现在只有gMoney:%d元\n' % (threading.current_thread().name, Money, gMoney))
            glock.release()
            print('gMoney:%d\n' % gMoney)


def main():
    for p in range(5):
        th_producer = Producer(name='生产者%d' % p)
        th_producer.start()

    for c in range(5):
        th_consumer = Consumer(name='消费者%d' % c)
        th_consumer.start()


if __name__ == '__main__':
    main()
