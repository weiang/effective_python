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

from collections import deque
import os
from Queue import Queue
import select
import subprocess
from threading import Lock
from threading import Thread
from time import sleep
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


# item 38

class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for j in range(5):
        args = (j, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


def item38():
    how_many = 10 ** 5
    counter = Counter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))

    how_many = 10 ** 5
    counter = LockingCounter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))
 

# item 39

class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super(Worker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            except:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super(StoppableWorker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
    
    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


def download(item):
    print("download...")
    return item


def resize(item):
    print("resize...")
    return item


def upload(item):
    print("upload...")
    return item


def item39():
#    download_queue = MyQueue()
#    resize_queue = MyQueue()
#    upload_queue = MyQueue()
#    done_queue = MyQueue()
#
#    threads = [
#            Worker(download, download_queue, resize_queue),
#            Worker(resize, resize_queue, upload_queue),
#            Worker(upload, upload_queue, done_queue)
#    ]
#
#    for thread in threads:
#        thread.start()
#
#    for _ in range(1000):
#        download_queue.put(object())
#
#    while len(done_queue.items) < 1000:
#        print('done=%d, Sleeping...' % len(done_queue.items))
#        sleep(0.01)
#
#    processed = len(done_queue.items)
#    polled = sum(t.polled_count for t in threads)
#    print('Processed ', processed, ' item after polling ', polled, 'times')

    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    upload_queue = ClosableQueue()
    done_queue = ClosableQueue()

    threads = [
            StoppableWorker(download, download_queue, resize_queue),
            StoppableWorker(resize, resize_queue, upload_queue),
            StoppableWorker(upload, upload_queue, done_queue)
    ]

    for thread in threads:
        thread.start()

    for _ in range(1000):
        download_queue.put(object())
    download_queue.close()
    download_queue.join()
    resize_queue.close()
    resize_queue.join()
    upload_queue.close()
    upload_queue.join()
    print(done_queue.qsize(), ' items finished')


def minimize():
    current = yield 
    while True:
        value = yield current
        current = min(value, current)


def item40():
    it = minimize()
    next(it)
    print(it.send(10))
    print(it.send(4))
    print(it.send(22))
    print(it.send(-1))


def main():
#    item36()
#    item37()
#    item38()
#    item39()
    item40()


if __name__ == '__main__':
    main()
