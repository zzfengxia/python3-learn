#!/usr/bin/env python3
# coding=utf-8

"""计算BMI指数;体重/身高(m)^2"""


def cala_bmi(height, weight, name="Francis", age=25, **kv):
    print("额外参数：", kv)
    h = float(height)
    w = float(weight)
    expont = w / (h * h)
    # 优化成lamda表达式？
    result = ''
    if expont > 32:
        result = '严重肥胖'
    elif expont > 28:
        result = '肥胖'
    elif expont > 25:
        result = '过重'
    elif expont > 18.5:
        result = '正常'
    else:
        result = '过轻'
    print("姓名:%s,年龄:%s,分析结果:%s" % (name, age, result))
