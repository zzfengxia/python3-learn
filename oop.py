#!/usr/bin/env python3
# coding: utf-8
# 第一个字符串为模块注释，可以使用__doc__访问
'python的面向对象特性'

# 可以使用__author__访问
__author__ = 'Francis.zz'

import types
from contextlib import contextmanager, closing
from urllib.request import urlopen


# 使用“_”或者“__”开头表示private属性，只是约定，仍然可以在外部访问
def _desc(dict):
    print('%s:%s' % (dict.name, dict.score))


'''
python使用class定义对象，参数为继承的对象。对象的所有方法第一个参数必须是self
在python中“__xxx__”这种形式的是特殊变量，外部可以访问。
“__xxx”是私有变量，外部无法直接访问。
“_xxx”是约定的私有变量，但是实际上外部可以直接访问。
'''


class User(object):
    # className是类变量
    className = 'User'

    # 对象的构造方法，self.__name是实例变量
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def desc(self):
        print('%s:%s' % (self.__name, self.__score))

    def get_grade(self):
        if self.__score > 85:
            print('grade:', 'A')
        elif self.__score > 65:
            print('grade:', 'B')
        else:
            print('grade:', 'C')


'''
对象继承
'''


class Animal(object):
    def desc(self):
        print('animal is running...')


class Dog(Animal):
    def desc(self):
        print('dog is running...')


class Cat(Animal):
    def desc(self):
        print('cat is running...')


'''
“file-like鸭子类型”，一个对象只要“看起来像鸭子，走起路来像鸭子”，那它就可以被看做是鸭子。
Car对象有desc方法，那么Car也可以当作是Animal的子类
'''


class Car(object):
    def desc(self):
        print('car is running...')


def print_desc(animal):
    animal.desc()


class Query(object):

    def __init__(self, name):
        self.name = name

    """ 实现上下文管理"""
    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)


@contextmanager
def h_tag(name):
    # 使用contextlib模块的contextmanager装饰器包装上下文
    print('<%s>' % name)
    yield
    print('</%s>' % name)


if __name__ == '__main__':
    # context, main
    main = "context"
    if "main" == main:
        user = User('Tom', 66)

        user.desc()
        user.get_grade()
        # 绑定实例变量
        user.className = 'subUser'
        print("user obj:%s" % user.className)
        print("User class:%s" % User.className)

        print_desc(Animal())
        print_desc(Car())
        print_desc(Cat())
        print_desc(Dog())

        # 查看对象类型
        print(type(123))
        print(type(user))
        print(type(print_desc))

        # 使用内置模块比较类型
        print(type(print_desc) == types.FunctionType)
        # 判断对象是某些对象中的一种
        print(isinstance((1, 2, 3), (list, tuple)))

        # 使用dir()获取对象的所有属性和方法
        print(dir(user))
        print(hasattr(user, 'desc'))
        setattr(user, 'name', "Jerry")
        print(user.name)
        print(getattr(user, 'sort', 404))

    elif "context" == main:
        with Query('Bob') as q:
            q.query()

        with h_tag('h'):
            print('Learning Python')

        # 使用closing使用对象变为上下文对象
        with closing(urlopen('https://www.baidu.com')) as page:
            for p in page:
                print(str(p, encoding='utf-8'))
