#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-04 22:44
# @desc   : 检查是否是位图文件

"""
BMP格式采用小端方式存储数据，文件头(前30个字节)的结构按顺序如下：

两个字节：'BM'表示Windows位图，'BA'表示OS/2位图；
一个4字节整数：表示位图大小；
一个4字节整数：保留位，始终为0；
一个4字节整数：实际图像的偏移量；
一个4字节整数：Header的字节数；
一个4字节整数：图像宽度；
一个4字节整数：图像高度；
一个2字节整数：始终为1；
一个2字节整数：颜色数。
"""
import struct


def check(f_name):
    with open(f_name, 'rb') as f:
        # 读取文件前30个字节
        data = f.read(30)
        if len(data) < 30:
            print('%s not a bmp file' % f_name)
            return False
        info = struct.unpack('<ccIIIIIIHH', data)
        if info[0] == b'B' and info[1] == b'M':
            print('%s is a bmp file' % f_name)
            return {
                'width': info[-4],
                'height': info[-3],
                'color': info[-1]
            }
        else:
            print('%s not a bmp file, flag:%s' % (f_name, info[:2]))


if __name__ == '__main__':
    print(check('C:\\Users\\Administrator\\Desktop\\24.bmp'))
