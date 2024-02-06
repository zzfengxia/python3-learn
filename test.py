#!/usr/bin/env python3
# coding: utf-8

import logging
# 使用python -m pdb test.py开启单步调试
from functools import reduce
from typing import Any

# 设置输出级别
logging.basicConfig(level=logging.INFO)


def str2num(s):
    logging.info("s:%s" % s)
    return int(s)


def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)


class SetOnceMappingMixin:
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._lc_kwargs = kwargs

    """自定义混入类"""
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)


class SetOnceDict(SetOnceMappingMixin, dict):
    """自定义字典"""
    pass


if __name__ == '__main__':
    print(chr(8888))
    # my_dict= SetOnceDict()
    # try:
    #     my_dict['username'] = 'jackfrued'
    #     my_dict['username'] = 'hellokitty'
    # except KeyError:
    #     pass
    # print(my_dict)
    # a = SetOnceDict(name='Tom')
    # print(a.get_name())