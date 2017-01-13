#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap4.py
Author: angwei(angwei@baidu.com)
Date: 2017/01/13 15:05:53
"""

from datetime import datetime, timedelta

# Item 29

class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super(VoltageResistance, self).__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super(BoundedResistance, self).__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


class FixedResistance(Resistor):
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota
    
def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

def item29():
    r = BoundedResistance(1e3)
#       r.ohms = 0
#    r2 = BoundedResistance(-5)
    r3 = FixedResistance(5)
#    r3.ohms = 10


def item30():
    bucket = Bucket(60)
    fill(bucket, 100)
    print(bucket)

    if deduct(bucket, 99):
        print("Had 99 quota")
    else:
        print("Not enough for 99 quota")
    print(bucket)


class Grade(object):
    def __init__(self):
        self._value = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        else:
            return self._value.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must between 0 and 100')
        self._value[instance] = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


def item31():
    first_exam = Exam()
    first_exam.writing_grade = 82
    second_exam = Exam()
    second_exam.writing_grade = 75
    print('First ', first_exam.writing_grade)
    print('Second ', second_exam.writing_grade)


def main():
#    item29()
#    item30()
    item31()


if __name__ == '__main__':
    main()

