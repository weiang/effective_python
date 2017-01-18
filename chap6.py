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

from contextlib import contextmanager
from functools import wraps
import logging

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


def item44():
    pass


def main():
#    item42()
#    item43()
    item44()


if __name__ == '__main__':
    main()
