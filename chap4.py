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

import json
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


# Item 32
class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super(LoggingLazyDB, self).__getattr__(name)


class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super(ValidatingDB, self).__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value


class SavingDB(object):
    def __setattr__(self, name, value):
        super(SavingDB, self).__setattr__(name, value)


class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super(LoggingSavingDB, self).__setattr__(name, value)

    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super(LoggingSavingDB, self).__getattr__(name)

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return super(LoggingSavingDB, self).__getattribute__(name)


class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]


class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        data_dict = super(DictionaryDB, self).__getattribute__('_data')
        return data_dict[name]


def item32():
    data = LazyDB()
    print('Before:', data.__dict__)
    print('foo: ', data.foo)
    print('After:', data.__dict__)

    data = LoggingLazyDB()
    print('exists:', data.exists)
    print('foo:', data.foo)
    print('foo:', data.foo)

    data = ValidatingDB()
    print('exists:', data.exists)
    print('foo:', data.foo)
    print('foo:', data.foo)

    print('----------')
    data = LoggingLazyDB()
    print('Before:', data.__dict__)
    print('foo exists:', hasattr(data, 'foo'))
    print('After:', data.__dict__)
    print('foo exists:', hasattr(data, 'foo'))

    print('----------')
    data = ValidatingDB()
    print('foo exists:', hasattr(data, 'foo'))
    print('foo exists:', hasattr(data, 'foo'))
    
    print('----------')
    data = LoggingSavingDB()
    print('Before:', data.__dict__)
    data.foo = 5
    data.foo
    print('After:', data.__dict__)
    data.foo = 7
    print('Finally:', data.__dict__)

    print('----------')
    data = BrokenDictionaryDB({'foo': 3})
#    data.foo
    data = DictionaryDB({'foo': 4})
    print('foo:', data.foo)


class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases != (object, ):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(object):
    __metaclass__ = ValidatePolygon
    sides = None
    
    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


def item33():
    print('Before class')
    class Line(Polygon):
        print('Before sides')
        sides = 1
        print('After sides')
    print('After class')


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        args = json.loads(json_data)['args']
        return cls(*args)


class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super(BetterPoint2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterPoint2D(%d, %d)' % (self.x, self.y)


class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })
    

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(json_data):
    params = json.loads(json_data)
    name = params['class']
    args = params['args']
    target_class = registry[name]
    return target_class(*args)


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super(EvenBetterPoint2D, self).__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'EvenBetterPoint2D(%d, %d)' % (self.x, self.y)

register_class(EvenBetterPoint2D)


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class RegisteredSerializable(BetterSerializable):
    __metaclass__ = Meta


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super(Vector3D, self).__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return 'Vector3D(%d, %d, %d)' % (self.x, self.y, self.z)


def item34():
    point = Point2D(5, 3)
    print('Object: ', point)
    print('Serialzied: ', point.serialize())

    point = BetterPoint2D(5, 3)
    print('Before: ', point)
    data = point.serialize()
    print('Serialized: ', data)
    after = BetterPoint2D.deserialize(data)
    print('After: ', after)

    point = EvenBetterPoint2D(5, 2)
    print('Before: ', point)
    data = point.serialize()
    print('Serialized ', data)
    after = deserialize(data)
    print('After: ', after)

    v3 = Vector3D(10, -7, 3)
    print('Before: ', v3)
    data = v3.serialize()
    print('Serialized:', data)
    print('After: ', deserialize(data))


class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta2(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(object):
    __metaclass__ = Meta2
    

class Customer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


def item35():
    foo = Customer()
    print('Before:', repr(foo.first_name), foo.__dict__)
    foo.first_name = 'Euclid'
    print('After:', repr(foo.first_name), foo.__dict__)


def main():
#    item29()
#    item30()
#    item31()
#    item32()
#    item33()
#    item34()
    item35()


if __name__ == '__main__':
    main()

