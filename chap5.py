#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap5.py
Author: angwei(angwei@baidu.com)
Date: 2017/01/16 10:41:39
"""

import os
import select
import subprocess
from threading import Thread
from time import time

# item36

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc


def run_openssl(data):
    env = os.environ.copy()
    env['password'] = 'xxx'
    proc = subprocess.Popen(
            ['openssl', 'enc', '-des3', '-pass', 'env:password'],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


def run_md5(input_stdin):
    proc = subprocess.Popen(
            ['md5'],
            stdin=input_stdin,
            stdout=subprocess.PIPE)
    return proc


def item36():
    proc = subprocess.Popen(
            ['echo', 'Hello from the child'],
            stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print(out.decode('utf-8'))

#    proc = subprocess.Popen(['sleep', '0.1'])
#    while proc.poll() is None:
#        print('Working...')
#    print('Exit status ', proc.poll())

    start = time()
    procs = []
    for _ in range(10):
        proc = run_sleep(0.1)
        procs.append(proc)
    for proc in procs:
        proc.communicate()
    end = time()
    print('Finished in %.3f seconds' % (end - start))

#    procs = []
#    for _ in range(3):
#        data = os.urandom(10)
#        proc = run_openssl(data)
#        procs.append(proc)
#    for proc in procs:
#        out, err = proc.communicate()
#        print(out[-10:])

    input_procs = []
    hash_procs = []
    for _ in range(3):
        data = os.urandom(10)
        proc = run_openssl(data)
        input_procs.append(proc)
        hash_proc = run_md5(proc.stdout)
        hash_procs.append(hash_proc)
    for proc in input_procs:
        proc.communicate()
    for proc in hash_procs:
        out, err = proc.communicate()
        print(out.strip())
        

# item 37
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


class FactorizeThread(Thread):
    def __init__(self, number):
        super(FactorizeThread, self).__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


def slow_systemcall():
    select.select([], [], [], 0.1)


def item37():
    numbers = [2139079, 1214759, 1516637, 1852285]
    start = time()
    for number in numbers:
        list(factorize(number))
    end = time()
    print('Took %.3f seconds' % (end - start))

    start = time()
    threads = []
    for number in numbers:
        thread = FactorizeThread(number)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end - start))

    start = time()
    for _ in range(5):
        slow_systemcall()
    end = time()
    print('Took %.3f seconds' % (end - start))

    start = time()
    threads = []
    for _ in  range(5):
        thread = Thread(target=slow_systemcall)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end -start))


def main():
#    item36()
    item37()


if __name__ == '__main__':
    main()

