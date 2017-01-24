#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap2.py
Author: work(work@baidu.com)
Date: 2017/01/06 09:59:23
"""

# Item 16  
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


# Item 17
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        result.append(value / float(total) * 100)
    return result


def read_visits(data_path):
    with open(data_path, "r") as f:
        for line in f:
            yield int(line)


def normalize_copy(numbers):
    numbers = list(numbers)
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / float(total)
        result.append(percent)
    return result


def normalize_func(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / float(total)
        result.append(percent)
    return result


class ReadVisits(object):
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        with open(self.path, "r") as f:
            for line in f:
                yield int(line)


# Item 18
def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ", ".join([str(x) for x in values])
        print("%s: %s" % (message, values_str))


# Item 21
def safe_division(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_div = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)
