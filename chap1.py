#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap1.py
Author: work(work@baidu.com)
Date: 2017/01/03 17:16:29
"""

def to_str(unicode_or_str):
    if isinstance(unicode_or_str, str)
        value = unicode_or_str
    else:
        value = unicode_or_str.encode("utf-8")
    return value


def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str
    else:
        value = unicode_or_str.decode("utf-8")
    return value

