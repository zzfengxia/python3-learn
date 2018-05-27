#!/usr/bin/env python3
# coding: utf-8

'枚举类'

from enum import Enum, unique

@unique
class WeekDay(Enum):
    Sun = 7
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

class Gender(Enum):
    Male = 0
    Female = 1

class Student(object):
    def __init__(self, name, gender):
        if not isinstance(gender, Gender):
            raise TypeError('illegal args gender')
        self.name = name
        self.gender = gender

if __name__ == "__main__":
    # 此种定义方式以1开始
    Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
    print(WeekDay.Tue)
    print(WeekDay(1))
    print(WeekDay['Wed'])

    print('type:', type(WeekDay))
    bart = Student('Bart', Gender.Male)
    if bart.gender == Gender.Male:
        print('测试通过!')
    else:
        print('测试失败!')

    d = {'a':1, 'b':2}
    print(d.a)
