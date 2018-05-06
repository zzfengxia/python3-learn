#!/usr/bin/env python3
# coding: "utf-8"

import bmi

n = input("您的名字：")
h = input("请输入您的身高(m)：")
w = input("请输入您的体重(kg)：")

bmi.cala_bmi(h, w, name=n, city='湖南', nature='汉')
