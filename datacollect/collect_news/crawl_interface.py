#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-30 17:45
@desc   : crawl_interface.py
"""

from typing import Protocol, runtime_checkable
from pandas import DataFrame


@runtime_checkable
class AbstractNewsCrawlData(Protocol):
    """
    新闻相关接口
    """

    def __init__(self):
        self.source_name = None

    def get_latest_news(self, top=None, plate=None, show_content=False) -> DataFrame:
        """
        获取当前最新新闻
        :param top:             前N条
        :param plate:           板块
        :param show_content:   是否显示具体内容
        :return:
        """
        pass

    def get_hot_news(self, top_n=None, plate=None) -> DataFrame:
        """
        获取当前最新热搜
        :param top_n:           前N条
        :param plate:           板块
        :return:
        """
        pass


@runtime_checkable
class AbstractStockCrawlData(Protocol):
    """
    股票相关接口
    """

    def __init__(self):
        self.source_name = None

    def get_latest_news(self, top=None, plate=None, show_content=False) -> DataFrame:
        """
        获取当前最新新闻
        :param top:             前N条
        :param plate:           板块
        :param show_content:   是否显示具体内容
        :return:
        """
        pass

    def get_hot_news(self, top_n=None, plate=None) -> DataFrame:
        """
        获取当前最新热搜
        :param top_n:           前N条
        :param plate:           板块
        :return:
        """
        pass

    def get_hot_stocks(self, top_n=None) -> DataFrame:
        """
        获取当前最新热搜
        :param top_n:           前N只热度排名最前的股票
        :return:
        """
        pass

    def get_guba_comments(self, stock_code, top_n=None, order_type=None) -> DataFrame:
        """
        获取当前最新热搜
        :param stock_code:      股票代码
        :param top_n:           前N条评论
        :param order_type:      排序方式，最新、最热
        :return:
        """
        pass
