#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2023-09-26 15:56
# @desc   : news_vars.py

# sina新闻入口：https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1
LATEST_URL = {'sina': 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=%s&k=&num=%s&page=1&r=%s'}
# LATEST_COLS = ['title','intro','ctime','intime','url']
LATEST_COLS = ['ctime', 'intime', 'title', 'url']
LATEST_COLS_C = ['ctime', 'intime', 'title', 'url', 'content']
NOTICE_INFO_URL = '%s%s/corp/view/%s?stock_str=%s'
NOTICE_INFO_CLS = ['title', 'type', 'date', 'url']
GUBA_SINA_URL = '%sguba.%s'
GUBA_SINA_COLS = ['title', 'content', 'ptime', 'rcounts']
# sina weibo热搜
HOT_NEWS_URL = {'sina': 'https://s.weibo.com/top/summary?cate=%s'}
HOT_NEWS_COLS = ['rank', 'keywords', 'tag', 'heat', 'url']
DEFAULT_SINA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Cookie": "SUB=_2AkMSTt6mf8NxqwJRmPERymrjbYl1wgDEieKkEi99JRMxHRl-yT9vqmZctRB6Oc7wSr40yb3BYbTdKI9fORNUFMlMPtgV; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5uBo4BixWfJ4D0dgrgL2SF; _s_tentry=passport.weibo.com; Apache=326951177099.8967.1695699346638; SINAGLOBAL=326951177099.8967.1695699346638; ULV=1695699346647:1:1:1:326951177099.8967.1695699346638:; UOR=,,www.google.com",
    "Host": "s.weibo.com"
}
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}
SINA_NEWS_TYPE = {'all': 2509, 'finance': 2516, 'stock': 2517, 'junshi': 2514}
SINA_HOT_TYPE = {'all': 'realtimehot'}

MAX_HOT_NUM = 50

GUBA_COMMENT = {'eastmoney': {'latest': 'https://guba.eastmoney.com/list,%s,f_%d.html',
                              'hottest': 'https://guba.eastmoney.com/list,%s_%d.html'}}
