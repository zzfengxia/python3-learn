#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 15:34
@desc   : get_news_all.py
"""

import inspect
import sys
from datacollect.collect_news.get_news_sina import *


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
    module = interface_class.__module__
    for name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj) and issubclass(obj, interface_class) and obj != interface_class:
            implementations.append(obj)
    return implementations


def process_news_data(method):
    def decorator(*args, **kwargs):
        all_subclasses = get_subclasses(AbstractNewsCrawlData)
        for subclass in all_subclasses:
            instance = subclass()
            if isinstance(instance, AbstractNewsCrawlData):
                df = method(instance, *args, **kwargs)
                if df is not None:
                    print(f'数据来源：{instance.source_name}')
                    print(df.to_string(index=False, justify='left'))
    return decorator


@process_news_data
def get_latest_news(instance, top=None, plate=None, show_content=False):
    return instance.get_latest_news(top, plate, show_content)


@process_news_data
def get_hot_news(instance, top=None, plate=None):
    return instance.get_hot_news(top, plate)
