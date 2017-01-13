#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: chap3.py
Author: angwei(angwei@baidu.com)
Date: 2017/01/13 09:30:49
"""

from collections import Sequence

# Item 28
class FrequencyList(list):
    def __init__(self, members):
        super(FrequencyList, self).__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts


class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class IndexableNode(BinaryNode):
    def _search(self, count, index):
        new_count = count 
        found = None
        
        # left first
        if self.left:
            found, new_count = self.left._search(new_count, index)

        # middle then
        if not found:
            if new_count == index:
                found = self
            else:
                found = None
                new_count += 1

        # right last 
        if (not found) and self.right:
            found, new_count = self.right._search(new_count, index)

        return (found, new_count)

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError("Index out of range") 
        return found.value


class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count


class BadType(Sequence):
    pass


class BetterNode(SequenceNode, Sequence):
    pass


def item28():
    foo = FrequencyList(['a', 'b', 'c', 'd', 'a', 'd'])
    print('Length is:', len(foo))

    foo.pop()
    print('After pop:', repr(foo))
    print('Frequency:', foo.frequency())

    # IndexableNode
    tree = IndexableNode(
            10,
            left=IndexableNode(
                5,
                left=IndexableNode(2),
                right=IndexableNode(
                    6, right=IndexableNode(7))),
            right=IndexableNode(
                15, left=IndexableNode(11)))
    print(list(tree))

    # SequenceNode
    seq = SequenceNode(
            10,
            left=SequenceNode(
                5,
                left=SequenceNode(2),
                right=SequenceNode(
                    6, right=SequenceNode(7))),
            right=SequenceNode(
                15, left=SequenceNode(11)))
    print("seq's len:", len(seq))

    better_node = BetterNode(
            10,
            left=SequenceNode(
                5,
                left=SequenceNode(2),
                right=SequenceNode(
                    6, right=SequenceNode(7))),
            right=SequenceNode(
                15, left=SequenceNode(11)))
    print('Index of 7 is', better_node.index(7))
    print('Count of 10 is', better_node.count(10))

def main():
    item28()


if __name__ == '__main__':
    main()
