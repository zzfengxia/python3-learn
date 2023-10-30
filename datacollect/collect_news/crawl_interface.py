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
class AbstractCrawlData(Protocol):
    def __init__(self):
        self.source_name = None

    def get_news(self, top=None, plate=None, show_content=False) -> DataFrame:
        pass
