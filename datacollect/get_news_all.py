#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 15:34
@desc   : get_news_all.py
"""
import functools
import inspect
import sys
import os
import importlib
from datacollect.collect_news.crawl_interface import AbstractNewsCrawlData
from datacollect.collect_news.get_news_sina import *
from datacollect.collect_news.get_news_douyin import *

# 动态导入包下的所以模块
# current_directory = os.path.dirname(__file__)
# # 获取包的绝对路径
# package_name = "datacollect.collect_news"
# package_path = os.path.join(current_directory, package_name.split('.')[-1])
# print(package_path)
# # 获取包下所有文件（不包括子目录）除了当前模块文件
# module_files = [file for file in os.listdir(package_path) if file.endswith(".py") and file != "__init__.py"]
#
# # 导入包下的所有模块
# for module_file in module_files:
#     module_name = os.path.splitext(module_file)[0]  # 去掉文件扩展名
#     module_path = f"{package_name}.{module_name}"  # 构造模块的完整路径
#     importlib.import_module(module_path)  # 动态导入模块


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
    @functools.wraps(method) # 保留原始函数的元信息
    def decorator(*args, **kwargs):
        all_subclasses = get_subclasses(AbstractNewsCrawlData)
        for subclass in all_subclasses:
            instance = subclass()
            if isinstance(instance, AbstractNewsCrawlData):
                df = method(instance, *args, **kwargs)
                if df is not None:
                    print()
                    print()
                    print(f'数据来源：{instance.source_name}')
                    print(df.to_string(index=False, justify='left'))

    return decorator


@process_news_data
def get_latest_news(instance, top=None, plate=None, show_content=False):
    return instance.get_latest_news(top, plate, show_content)


@process_news_data
def get_hot_news(instance, top=None, plate=None):
    return instance.get_hot_news(top, plate)
