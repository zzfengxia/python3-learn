#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import my_fun as fun
from collections import Iterable, namedtuple, deque, defaultdict, OrderedDict, Counter
import os

if __name__ == "__main__":
    # name = input('please enter your name:')
    # 使用""" """注释多行
    """print('''hello world!
    hey Francis
    are you ok?''')
    
    print("你好吗")"""

    L = list(range(1, 100, 2))
    # slice语法取前两个元素，[1:2)
    # print(L[1:3])
    # print(L[-2:])
    # 每隔5个元素取一个
    # print(L[::5])
    # print(L[10:50:2])
    # 对字符串切片，即截取字符串
    # print("ABCDEFG"[2:])

    # 迭代
    # print(isinstance('abc', Iterable))
    # for s in "ABCD":
    #     print(s)

    d = {"a": "Tom", "b": "Jerry", "c": "Lucy"}
    # for k, v in d.items():
    #     print(k, v)
    # for k in d:
    #     print(k)
    # for v in d.values():
    #     print(v)
    # for i, v in enumerate(['a', 'b', 'c', 'd']):
    #     print(i, v)

    # print(fun.min_max([1,5,3,10, 2]))


    # 列表生成式
    # print([p for p in os.listdir('.')])
    # print([m+':'+n for m in ["Tom", "Jerry"] for n in ["Amerecia", "Japen"]])
    # print([k + '=' + v for k, v in d.items()])
    # print([s.lower() for s in ("City", "Country", "Nature")])
    # print([x * x for x in [1, 2, 3, 4]])

    # print([s.lower() for s in ("City", "Country", "Nature", 2, "Tom") if isinstance(s, str)])


    # 生成器
    # gen = (x * x for x in range(10))
    # print(next(gen))

    # f = fun.fib(6)
    # for g in f:
    #    print(g)
    # t = fun.triangles2(10)
    # for l in t:
    #     print(l)

    # 模板字符串
    name = 'Francis'
    print(f'Hello, {name}')

    # NAMETUPLE, DEQUE, DEFAULT_DICT, ORDERED_DICT, COUNTER
    main = 'COUNTER'

    if main == 'NAMETUPLE':
        # 定义namedtuple命名元组
        Point = namedtuple('Point', ['x', 'y'])
        p1 = Point(21, 2)

        print('点坐标, x:%d, y:%d' % (p1.x, p1.y))
        field_names = 'a,b, c'
        if isinstance(field_names, str):
            field_names = field_names.replace(',', ' ').split()
            print(field_names)
        field_names = list(map(str, field_names))
        typename = 'Point'
        print([typename] + field_names)
    elif main == 'DEQUE':
        d = deque(['a', 'b', 'c'])
        d.append('e')
        d.appendleft('x')

        print(d.pop())
        print(d)

    elif main == 'DEFAULT_DICT':
        dd = defaultdict(lambda: 'N/A')
        dd['name'] = 'Francis'
        print(dd['name'])
        print(dd['age'])

    elif main == 'ORDERED_DICT':
        # 有序字典
        d = dict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
        print(d.popitem())
        # 按照添加顺序排序
        od = OrderedDict({'a': 1, 'b': 2, 'c': 3})
        print(od.popitem(last=False))

    elif main == 'COUNTER':
        # 计数器
        c = Counter(iter('helloworld'))
        print(c.pop('l'))
