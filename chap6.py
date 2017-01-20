#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap6.py
Author: angwei(angwei@baidu.com)
Date: 2017/01/18 16:15:04
"""

from bisect import *
from collections import deque
from collections import OrderedDict
from contextlib import contextmanager
import copy_reg
from decimal import * 
from functools import wraps
from heapq import heappush, heappop
import logging
import pickle

# item 42

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


def item42():
    fibonacci(10)


def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


def item43():
    with debug_logging(logging.DEBUG):
        print('Inside:')
        my_function()
    print('After:')
    my_function()

    print('-------------------')
    with log_level(logging.DEBUG, 'my-log') as logger:
        logger.debug('This is my message')
        logging.debug('This will not print')
    logger = logging.getLogger('my-log')
    logger.debug('Debug will not print')
    logger.error('Error will print')


class BetterGameState(object):
    def __init__(self, level=0, points=0, magic=5):
        self.level = level 
        self.points = points 
        self.magic = magic


def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        kwargs.pop('lives')
    return BetterGameState(**kwargs)


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


def item44():
#    state = GameState()
    
#    copy_reg.pickle(GameState, pickle_game_state)
    state_path = 'game_state.bin'

#    with open(state_path, 'wb') as f:
#        pickle.dump(state, f)

    with open(state_path, 'rb') as f:
        state_after = pickle.load(f)
    print(state_after.__dict__)
    
#    serialized = pickle.dumps(state)
#    state_after = pickle.loads(serialized)
#    print(state_after.__dict__)

#    state = GameState()
#    state.points += 1000
#    serialized = pickle.dumps(state)
#    state_after = pickle.loads(serialized)
#    print(state_after.__dict__)


def item46():
    fifo = deque()
    fifo.append(1)
    x = fifo.popleft()
    
    a = OrderedDict()
    b = OrderedDict()
    a['foo'] = 1
    a['bar'] = 2
    b['foo'] = 'red'
    b['bar'] = 'blue'

    for x in zip(a.values(), b.values()):
        print("%r\t%r" % (x[0], x[1]))

    a = []
    heappush(a, 5)
    heappush(a, 3)
    heappush(a, 7)
    heappush(a, 4)

    print('Before:', a)
    a.sort()
    print('After:', a)
    print(heappop(a), heappop(a), heappop(a), heappop(a))

    x = list(range(10**6))
    i = bisect_left(x, 991234)
    print("index=%d" % (i))


def item47():
    rate = Decimal('1.45')
    seconds = Decimal('222')
    cost = rate * seconds / Decimal('60')
    print(cost)
    rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
    print(rounded)

    rate = Decimal('0.05')
    seconds = Decimal('5')
    cost = rate * seconds / Decimal('60')
    print(cost)
    rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
    print(rounded)
    pass


def main():
#    item42()
#    item43()
#    item44()
#    item46()
    item47()


if __name__ == '__main__':
    main()
