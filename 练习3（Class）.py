# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   练习3（Class）.py
@Desc:
@Create: 2020/08/13 15:11
"""
import datetime
from dateutil import rrule
import itertools  # 迭代器

iterobj = itertools.count(start=10)
print(next(iterobj))


# 生成器
class generatorDate:

    @staticmethod
    def fibs():
        prev, curr = 0, 1
        while True:
            yield prev
            prev, curr = curr, prev + curr

    @staticmethod
    def g():
        yield 0
        yield 1
        yield 2


print(generatorDate.g())
print(generatorDate.g().__next__())
print(next(generatorDate.g()))

print(list(itertools.islice(generatorDate.fibs(), 10)))

# 集合解析
gt = {x ** 2 for x in range(10)}
# 生成器解析
gt1 = (x ** 2 for x in range(10))
print('typeofgt:', type(gt))
print('gt:', gt)
print('typeofgt1:', type(gt1))
print('gt1:', gt1)


# 类方法
class Bar:
    @classmethod
    def method(cls, x):
        print(cls)


# 静态方法
class Bar1:
    @staticmethod
    def add():
        print('add')


class CalculationDate:
    def __init__(self, start_date, end_date):
        self.start = datetime.datetime.strptime(start_date, "%Y,%m,%d")
        self.end = datetime.datetime.strptime(end_date, "%Y,%m,%d")

    def days(self):
        d = self.end - self.start
        return d.days if d.days > 0 else False

    def weeks(self):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=self.start, until=self.end)
        return weeks.count()


fir_twe = CalculationDate("2019,5,1", "2019,11,25")
day = fir_twe.days()
week = fir_twe.weeks()
print("CalculationDate: 2019-5-1,2019-11-25:")
print("day:", day)
print("week:", week)


class Date(object):
    def __init__(self, year=0, month=0, day1=0):
        self.year = year
        self.month = month
        self.day1 = day1

    @classmethod
    def from_string(cls, date_as_string):
        year, month, day1 = map(int, date_as_string.split('-'))
        date = cls(year, month, day1)
        return date

    @staticmethod
    def is_date(date_as_string):
        year, month, day1 = map(int, date_as_string.split('-'))
        return day1 <= 31 and month <= 12 and year <= 2050


d = Date.from_string('2020-09-06')
is_date = Date.is_date('2020-09-06')
print(d)
print(d.year)
print(d.month)
print(d.day1)
print(is_date)


# 类继承
class A:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def eat():
        return 'meat'


class B(A):
    # # 写法一
    # def __init__(self, name, age):
    #     self.age = age
    #     A.__init__(self, name)

    # 写法二
    def __init__(self, name, age):
        self.age = age
        super().__init__(name)


b = B("zhangsan", 24)
print(b.name)
print(b.age)
print(b.eat())


class physicist:
    def __init__(self, name):
        self.name = name


class experimental_physicist(physicist):
    pass


class theoretical_physicist(physicist):
    pass


class bar:
    # 限制属性，固定并且只读
    __slots__ = {'name', 'age', 'gender'}


class attr:
    def __getattr__(self, item):
        print("getattr")

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        print(self.__dict__)


attr1 = attr()
attr1.name = 'lisi'


class Fibs:
    def __init__(self, max):
        self.max = max
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib


# 迭代器，还没放到内存当中
fibs = Fibs(1000000)
# 从内存中取出
lst = [fibs.__next__() for i in range(10)]
print(lst)
