#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 17:16
@desc   : my_class.py
"""

from typing import Protocol, runtime_checkable
import inspect
import sys


@runtime_checkable
class MyProtocol(Protocol):
    def execute(self) -> None:
        pass


class MyClass1:
    def execute(self) -> None:
        print("MyClass1 executed")


class MyClass2:
    def execute(self) -> None:
        print("MyClass2 executed")


# 获取实现了 MyProtocol 协议的所有类
def get_protocol_implementations(protocol_class):
    implementations = []
    for name, obj in globals().items():
        if isinstance(obj, type) and issubclass(obj, protocol_class) and obj != protocol_class:
            implementations.append(obj)
    print(f'implementations:{implementations}')
    return implementations


def get_protocol_implementations2(protocol_class):
    implementations = []
    module = protocol_class.__module__
    for name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj) and issubclass(obj, protocol_class) and obj != protocol_class:
            implementations.append(obj)
    print(f'implementations:{implementations}')
    return implementations


# 获取并执行实现了 MyProtocol 协议的所有类的方法
if __name__ == "__main__":
    implementations = get_protocol_implementations(MyProtocol)
    for implementation in implementations:
        instance = implementation()
        instance.execute()
