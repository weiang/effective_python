#!/usr/bin/env python
# -*- encoding=utf-8 -*-

import os
import json
from collections import Sequence
from threading import Thread

# Item 24
class InputData(object):
    def read(self):
        raise NotImplementedError


class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super(PathInputData, self).__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    for file in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, file))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class GenericPathInputData(GenericInputData):
    def __init__(self, path):
        super(GenericPathInputData, self).__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        for input_file in os.listdir(config['data_dir']):
            yield cls(os.path.join(config['data_dir'], input_file))


class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_data_class, config):
        raise NotImplementedError


class GenericLineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

    @classmethod
    def create_workers(cls, input_data_class, config):
        workers = []
        for input_data in input_data_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


def generic_mapreduce(worker_class, input_data_class, config):
    workers = worker_class.create_workers(input_data_class, config)
    return execute(workers)


def item24():
    config = { "data_dir": "." }
    print generic_mapreduce(GenericLineCountWorker, GenericPathInputData, config)
    print mapreduce(".")


# Item 25
class Base(object):
    def __init__(self, value):
        self.value = value


class PlusTwo(Base):
    def __init__(self, value):
        super(PlusTwo, self).__init__(value)
        self.value += 2


class TimeFive(Base):
    def __init__(self, value):
        super(TimeFive, self).__init__(value)
        self.value *= 5


class Value(TimeFive, PlusTwo):
    def __init__(self, value):
        super(Value, self).__init__(value)
        print "(%d + 2) * 5 = %d" % (value, self.value)


# Item 26
class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict() 
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, **kwargs):
        self.value = value
        self.left = kwargs.pop('left', None)
        self.right = kwargs.pop('right', None)


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, **kwargs):
        left = kwargs.pop('left', None)
        right = kwargs.pop('right', None)
        parent = kwargs.pop('parent', None)

        super(BinaryTreeWithParent, self).__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            return value.value
        else:
            return super(BinaryTreeWithParent, self)._traverse(key, value)


class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, **kwargs):
        self.cores = kwargs.pop('cores', None)
        self.ram = kwargs.pop('ram', None)
        self.disk = kwargs.pop('disk', None)


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, **kwargs):
        self.ports = kwargs.pop('ports', None)
        self.speed = kwargs.pop('speed', None)


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
                Machine(**kwargs) for kwargs in machines]


def item25():
    tree = BinaryTree(10, 
            left=BinaryTree(7, right=BinaryTree(9)),
            right=BinaryTree(13, left=BinaryTree(11)))
    print(tree.to_dict())

    root = BinaryTreeWithParent(10)
    root.left = BinaryTreeWithParent(7, parent=root)
    root.left.right = BinaryTreeWithParent(9, parent=root.left)
    print(root.to_dict())

    my_tree = NamedSubTree('foobar', root.left.right)
    print(my_tree.to_dict())


    serialized  =  """{ 
        "switch": { "ports": 5,  "speed": 1e9 },
        "machines": [
            {"cores": 8, "ram": 32e9, "disk": 5e12}, 
            {"cores": 4, "ram": 16e9, "disk": 1e12},
            {"cores": 2, "ram": 4e9, "disk": 500e9}
        ]
    }"""

    deserialized = DatacenterRack.from_json(serialized)
    roundtrip = deserialized.to_json()
    #print roundtrip
    assert json.loads(serialized) == json.loads(roundtrip)


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
#    item24()
    item25()
    item28()
    

if __name__ == '__main__':
    main()

