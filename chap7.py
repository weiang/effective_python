#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap7.py
Author: angwei(angwei@baidu.com)
Date: 2017/01/20 11:26:05
"""

def palindrome(word):
    """Return True if the given word is a palindrome."""
    return word == word[::-1]


def item49():
    print(repr(palindrome.__doc__))


def main():
    item49()


if __name__ == '__main__':
    main()

