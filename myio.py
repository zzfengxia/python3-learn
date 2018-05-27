#!/usr/bin/env python3
# coding: utf-8

from io import StringIO
from io import BytesIO
import os

# 搜索文件名包含指定关键字的文件
def find_file(dir, name):
    fl = os.listdir(dir)
    for f in fl:
        fname = os.path.join(dir, f)
        if os.path.isdir(f):
            find_file(f, name)
        elif os.path.isfile(f):
            if name in f:
                print(fname)


if __name__ == '__main__':
    with open('D:\\workspaces\\python3\\python3-learn\\bmi.py', 'r', encoding='utf-8') as f:
        for l in f.readlines():
            print(l.strip())

# string io
    sf = StringIO()
    sf.write('hello')
    sf.write(' world!')
    print(sf.getvalue())

    bf = BytesIO()
    bf.write('你好'.encode('utf-8'))
    print(bf.getvalue())
    f = BytesIO(b'\xe4\xbd\xa0\xe5\xa5\xbd')
    print(f.read().decode('utf-8'))

    # 获取系统信息
    print('系统：', os.name)
    print('环境变量：', os.environ.get('PYTHON_HOME'))

    print('绝对路径：', os.path.abspath('.'))
    # 然后创建一个目录:
    #os.mkdir('D:\\workspaces\\python3\\python3-learn\\aa')
    #os.rmdir('D:\\workspaces\\python3\\python3-learn\\aa')
    print('合并路径：', os.path.join('usr', 'local'))
    print('拆分路径：', os.path.split('D:\\workspaces\\python3\\python3-learn\\myio.py'))
    print('文件扩展名：', os.path.splitext('D:\\workspaces\\python3\\python3-learn\\myio.py'))

    # 对文件重命名
    #os.rename('test.txt', 'test.py')
    # 删掉文件
    #os.remove('test.py')
    print('过滤当前目录下所有目录：', [x for x in os.listdir('.') if os.path.isdir(x)])
    print('过滤当前目录下所有.py文件：', [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'])

    find_file('D:\\workspaces\\python3\\python3-learn', 'oop')
