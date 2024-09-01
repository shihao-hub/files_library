import collections
import itertools
import time
import unittest
from collections import defaultdict

from box import Box, BoxList, ConfigBox, BoxError, BoxKeyError, SBox
from typing_extensions import TypedDict


# class Test(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass


class DogHelper:
    def _print(self):
        this = self
        print(123)

    def _print2(self):
        pass


class Dog(DogHelper):
    def __init__(self):
        self._print()

    class InnerDog:
        name = "inner dog"


class DemoHelper:
    def _demo_details(self):
        this = self
        return "DemoHelper:_demo_details"


class Demo(DemoHelper):
    def __init__(self):
        self._demo_details()

    def __private(self):
        pass


def test():
    print(locals())

    def test2():
        pass

    print(locals())


if __name__ == '__main__':
    # print(time.time() + 1)
    # args = [1, 2, 3]
    # print([4, *args])
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    #
    # for e in itertools.chain([0, 1], [2, 3]):
    #     print(e)
    # print(Dog.InnerDog.name)
    # print(Dog())

    # dic = defaultdict(None, **dict(a=1, b=2))

    box = Box(**dict(
        name="zsh",
        age=24,
    ))
    print(box.get("name"))
    print(box["age"])
    for k, v in box.items():
        print(k, v)
    print(box.get("items"))
    print(time.time())
    print("----------------")
    # test()

    # const = Box(**dict(
    #     data={"id": 123}
    # ))
    # print(const.data)

    const = collections.namedtuple("const", [
        "data"
    ])(**dict(
        data={"id": 123}
    ))
    print(type(object()))
    print(type(const))

    print(const.__slots__)
    print(tuple(const))

    print({k: v for k, v in zip(const._fields, tuple(const))})
    print(dict(const._asdict()))

    # const_dict = const._asdict()
    # print(const_dict)
    # print(dict(const_dict))
    # print(dict(const))
    # print(const_dict.keys())
    # print(const_dict.values())
    # print(type(const_dict))

    # const2 = collections.namedtuple("const", [
    #     "data"
    # ])(**dict(
    #     data={"id": 123}
    # ))
    #
    # print(const.data)
    # print(const2.data)
    #
    # Point = collections.namedtuple('Point', ['x', 'y'])
    # Point2 = collections.namedtuple('Point', ['x', 'y'])
    #
    # print(Point(1, 2))
    # print(Point2(1, 2))
    # print(id(Point), id(Point2))
