#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-18 17:30
@desc   : local_api_test.py
"""

import datacollect


if __name__ == '__main__':
    #print(datacollect.get_latest_news(top=10, plate='stock').to_string(index=False, justify='left'))
    #datacollect.get_latest_news(top=10, plate='stock')
    # datacollect.get_hot_news(top=10)
    datacollect.get_guba_comments('300785', top_n=20)




