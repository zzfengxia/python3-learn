#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2018-06-03 12:06
# @desc   : python正则表达式

import re


if __name__ == '__main__':
    al = re.split(r'[\s,;]+', 'a,b  c;d   e')
    print(al)

    # 先编译正则表达式
    re_telphone = re.compile(r'^(\d{3})-(\d{3,8})$')

    print(re_telphone.match("024-2418756").groups())
    print(re_telphone.match("024-1387453").groups())