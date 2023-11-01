#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-18 17:30
@desc   : local_api_test.py
"""

import datacollect
import datacollect.collect_news as cn


if __name__ == '__main__':
    #print(datacollect.get_latest_news(top=10, plate='stock').to_string(index=False, justify='left'))
    #cn.get_latest_news(top=10, plate='stock')
    cn.get_hot_news()




