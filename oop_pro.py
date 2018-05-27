#!/usr/bin/env python3
# coding: utf-8

'pyhon面向对象高级编程'

__author__='Francis.zz'

import types

# 定义类，动态绑定属性
class Student(object):
    # 使用__slots__限制实例属性，对类没有限制作用，对其子类没有限制作用
    __slots__ = ('name', 'score', 'set_score')

    # 特殊函数, toString方法
    def __str__(self):
        return '%s:%s' % (self.name, self.score)

    pass

class Animal(object):
    # 使用@property定义属性
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise valueError('color attr must be string')
        self._color = value

    # 没有定义setter方法的只读属性
    @property
    def age(self):
        return 8

class DynamicApi(object):
    def __init__(self, url=''):
        self.url = url

    # 链式调用。找不到属性时调用该方法
    def __getattr__(self, val):
        return DynamicApi('%s/%s' % (self.url, val))

    # 使对象变成像方法一样调用
    def __call__(self, args):
        return DynamicApi('%s/%s' % (self.url, args))

    def __str__(self):
        return self.url

def set_score(self, num):
    self.score = num

if __name__ == '__main__':
    # 绑定实例变量
    lucy = Student()
    lucy.name = 'Lucy'
    lucy.score = 80

    print(lucy.name)
    # 调用__str__方法
    print(lucy)
    # 绑定类变量
    Student.grade = 3

    print(lucy.grade)

    # 绑定实例方法,需要借助types.MethodType方法,把实例变量set_score指向set_score方法
    frank = Student()
    frank.set_score = types.MethodType(set_score, frank)

    frank.set_score(98)
    print('Frank:', frank.score)

    # 绑定类方法
    Student.set_score = set_score

    lucy.set_score(85)
    print('Lucy:', lucy.score)

    cat = Animal()
    cat.color = 'Red'
    # 无法对只读属性赋值
    #cat.age = 10
    print('color', cat.color)
    print('age:', cat.age)

    # 链式调用
    print(DynamicApi().api.user('lisa').registy)






