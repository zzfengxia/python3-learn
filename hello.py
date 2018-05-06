#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import my_fun as fun
from collections import Iterable
import os

#name = input('please enter your name:')
# 使用""" """注释多行
"""print('''hello world!
hey Francis
are you ok?''')

print("你好吗")"""


L = list(range(1, 100, 2))
# slice语法取前两个元素，[1:2)
#print(L[1:3])
#print(L[-2:])
# 每隔5个元素取一个
#print(L[::5])
#print(L[10:50:2])
# 对字符串切片，即截取字符串
#print("ABCDEFG"[2:])


print(fun.trim(" 你好   ") == "你好")


# 迭代
# print(isinstance('abc', Iterable))
# for s in "ABCD":
#     print(s)

d = {"a":"Tom", "b":"Jerry", "c":"Lucy"}
# for k, v in d.items():
#     print(k, v)
# for k in d:
#     print(k)
# for v in d.values():
#     print(v)
# for i, v in enumerate(['a', 'b', 'c', 'd']):
#     print(i, v)

#print(fun.min_max([1,5,3,10, 2]))


# 列表生成式
#print([p for p in os.listdir('.')])
#print([m+':'+n for m in ["Tom", "Jerry"] for n in ["Amerecia", "Japen"]])
#print([k + '=' + v for k, v in d.items()])
#print([s.lower() for s in ("City", "Country", "Nature")])
#print([x * x for x in [1, 2, 3, 4]])

#print([s.lower() for s in ("City", "Country", "Nature", 2, "Tom") if isinstance(s, str)])


# 生成器
gen = (x * x for x in range(10))
#print(next(gen))

#f = fun.fib(6)
#for g in f:
#    print(g)
t = fun.triangles2(10)
for l in t:
    print(l)


