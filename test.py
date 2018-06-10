#!/usr/bin/env python3
# coding: utf-8

# 使用python -m pdb test.py开启单步调试
from functools import reduce
import logging

# 设置输出级别
logging.basicConfig(level=logging.INFO)


def str2num(s):
    logging.info("s:%s" % s)
    return int(s)


def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)


def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 8')
    print('99 + 88 + 8 =', r)


main()
