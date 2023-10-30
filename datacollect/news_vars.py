#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2023-09-26 15:56
# @desc   : news_vars.py

# sina新闻入口：https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1
LATEST_URL = {'sina': 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=%s&k=&num=%s&page=1&r=%s'}
#LATEST_COLS = ['title','intro','ctime','intime','url']
LATEST_COLS = ['ctime','intime','title','url']
LATEST_COLS_C = ['ctime','intime','title','url','content']
NOTICE_INFO_URL = '%s%s/corp/view/%s?stock_str=%s'
NOTICE_INFO_CLS = ['title', 'type', 'date', 'url']
GUBA_SINA_URL = '%sguba.%s'
GUBA_SINA_COLS = ['title', 'content', 'ptime', 'rcounts']

SINA_NEWS_TYPE = {'all': 2509, 'finance': 2516, 'stock': 2517, 'junshi': 2514}
