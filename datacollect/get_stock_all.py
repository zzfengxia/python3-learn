#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-11-10 15:30
@desc   : get_stock_all.py
"""

import inspect
import sys
import os
import importlib
from datacollect.collect_news.crawl_interface import AbstractStockCrawlData
from datacollect.collect_news.get_stock_eastmoney import *


def get_subclasses(protocol_class):
    implementations = []
    for name, obj in globals().items():
        if isinstance(obj, type) and issubclass(obj, protocol_class) and obj != protocol_class:
            implementations.append(obj)
    return implementations


def get_subclasses2(interface_class):
    """
    # 获取实现了 AbstractCrawlData 接口的所有子类，这种方式只能获取到所有实现类都写到同一个文件中
    :param interface_class:
    :return:
    """
    implementations = []
    for name, obj in inspect.getmembers(sys.modules[interface_class.__module__]):
        if inspect.isclass(obj) and issubclass(obj, interface_class) and obj != interface_class:
            implementations.append(obj)
    return implementations


def process_news_data(method):
    def decorator(*args, **kwargs):
        all_subclasses = get_subclasses(AbstractStockCrawlData)
        for subclass in all_subclasses:
            instance = subclass()
            if isinstance(instance, AbstractStockCrawlData):
                df = method(instance, *args, **kwargs)
                if df is not None:
                    print()
                    print()
                    print(f'数据来源：{instance.source_name}')
                    print(df.to_string(index=False, justify='left'))

    return decorator


@process_news_data
def get_guba_comments(instance, stock_code, top_n=None, order_type=None):
    return instance.get_guba_comments(stock_code, top_n, order_type)
