#!/usr/bin/env python3
# coding:utf-8

import my_fun as fun
import time
from collections import Iterable

#print(list(fun.spell_check(['ANHS', 'aiUr', 'nglr', 'TshT'])))

#print(fun.prod([1, 2, 3, 5, 6]))

#print(fun.str2float('1232.456'))





#print(list(fun.is_palindrome(range(1, 100))))

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

#print(sorted(L))
#print(sorted(L, key=lambda x:x[1], reverse=True))

counterA = fun.createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = fun.createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

@fun.metric
def aa():
    time.sleep(0.1)
    print("111")

aa()
