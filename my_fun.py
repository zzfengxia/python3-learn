#!usr/bin/env python3
# coding= "utf-8"

import time
import functools

"""阶乘"""
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


'''递归优化--尾递归'''
def fact_iter(n, factor):
    if n == 1:
        return factor
    else:
        return fact_iter(n - 1, factor * n)


''' 递归实现汉诺塔 '''
def hanoi_move(n, a, b, c):
    if n == 1:
        print(a, "-->", c)
    else:
        hanoi_move(n - 1, a, c, b)
        hanoi_move(1, a, b, c)
        hanoi_move(n - 1, b, a, c)

# 使用递归+slice切片实现去除字符串首尾空格的方法
def trim(s):
    if s[:1] == " ":
        return trim(s[1:])
    if s[-1:] == " ":
        return trim(s[:-1])
    return s


def min_max(L):
    if len(L) == 0:
        return None, None
    min = L[0]
    max = L[0]
    for n in L:
        if(n > max):
            max = n
        if(n < min):
            min = n
    return min, max


# 斐波拉契数列的前frontNum个数列生成器。函数定义中包含yield，那么这个函数就是一个generator
def fib(frontNum):
    a, b = 0, 1
    for n in range(frontNum):
        # 函数体中使用yield定义生成器
        yield b
        # 这里相当于t = (b, a + b) # t是一个tuple，a = t[0]，b = t[1]
        a, b = b, a + b

    return 'done'


# 杨辉三角,行生成器
def triangles(maxLine):
    out = [1]
    for n in range(maxLine):
        yield out
        length = len(out)
        b = out[:-1]
        f = out[1:]
        out = [1]
        for i in range(length - 1):
            out.append((b[i] + f[i]))

        out.insert(length, 1)

    return 'done'

# 优化后的杨辉三角生成器
def triangles2(maxLine):
    out = [1]
    for x in range(maxLine):
        yield out
        out = [1] + [a + b for a, b in zip(out[:-1], out[1:])] + [1]

    return 'done'


# 简单Lambda表达式
def ld_fun(x, y, f):
    return f(x) + f(y)


# 使用map函数实现首字母大写，其他小写
def spell_check(L):
    return map(lambda s:s[:1].upper() + s[1:].lower(), L)


# 列表求积
def prod(L):
    return reduce(lambda x, y:x * y, L)


# 字符串转换为浮点数
def str2float(ss):
    return reduce(lambda x, y:x + y*pow(10, -len(str(y))), map(int, ss.split('.')))

# 从3开始的基数生成器
def cardinal():
        n = 1
        while True:
            n = n + 2
            yield n

# 素数生成器
def primes():
    def not_divisible(n):
        return lambda x: x % n > 0
    # 第一个为2
    yield 2
    it = cardinal()
    while True:
        n = next(it)
        yield n
        it = filter(not_divisible(n), it)

# 筛选回数，切片的第三个参数为负数时，表示从右至左切片
def is_palindrome(ite):
    return filter(lambda x: str(x)[::1] == str(x)[::-1], ite)


# 返回计数器函数
def createCounter():
    n = 0
    def count():
        nonlocal n
        n = n + 1
        return n
    return count


# 装饰器，打印函数执行时间
def metric(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kw):
        start = int(round(time.time() * 1000))
        result = fun(*args, **kw)
        end = int(round(time.time() * 1000))
        print("fun %s executed %s ms" % (fun.__name__, (end - start)))
        return result
    return wrapper

