# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

"""
Miscellaneous utilities.
"""

import functools


def memoize(func):
    """
    Memoization of an arbitrary function
    """
    cache = dict()
    @functools.wraps(func)
    def _wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return _wrapper


class Singleton(type):
    """
    Singleton metaclass
    """
    def __new__(metacls, name, bases, attrs):
        # pylint: disable=C0103
        cls = type.__new__(metacls, name, bases, attrs)
        cls.__eq__ = lambda self, other: other is self
        cls.__lt__ = lambda self, other: not other is self
        cls.__copy__ = lambda self: self
        cls.__deepcopy__ = lambda self, memo: self
        cls.__repr__ = lambda self: self.__reprval__
        cls.__len__ = lambda self: len(self.__reprval__)
        cls.__hash__ = lambda self: hash(id(self))
        return functools.total_ordering(cls)()


def callbackByName(funcName):
    def _wrapper(instance, *args, **kwargs):
        return getattr(instance, funcName)(*args, **kwargs)
    return _wrapper


def chars(s):
    return (s, s.encode('ascii')[0])
