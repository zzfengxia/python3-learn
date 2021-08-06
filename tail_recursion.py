#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-07-26 17:55
# @desc   : 


def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


def factorial_tail(n, total):
    # 尾递归
    if n == 1:
        return total
    return factorial_tail(n - 1, n * total)


def factorial2(n):
    return factorial_tail(n, 1)


def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_tail(n, t1, t2):
    # 尾递归
    if n <= 1:
        return t2
    return fibonacci_tail(n - 1, t2, t1 + t2)


if __name__ == '__main__':
    for i in range(10):
        print(fibonacci(i), end=' ')
    print()
    for i in range(10):
        print(fibonacci_tail(i, 1, 1), end=' ')
    ele = [1, 3, 10]
    print(isinstance(ele, list))