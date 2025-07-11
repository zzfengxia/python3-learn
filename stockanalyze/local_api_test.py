#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-18 17:30
@desc   : local_api_test.py
"""

import datacollect
import akshare as ak
import sys
import threading


def input_with_timeout(prompt, timeout, default):
    user_input = [default]

    def get_input():
        try:
            user_input[0] = input(prompt)
        except Exception:
            pass
    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    return user_input[0] if user_input[0] else default


if __name__ == '__main__':
    #res = ak.stock_zt_pool_em(date='20231116')
    #res.to_excel("C:\\Users\\86153\\Desktop\\20231116.xlsx")
    #print(datacollect.get_latest_news(top=10, plate='stock').to_string(index=False, justify='left'))
    #datacollect.get_latest_news(top=10, plate='stock')
    # datacollect.get_hot_news(top=10)
    code_input = input_with_timeout("输入代码（默认1表示上证指数）：", 3, "1")
    code = "sh000001" if code_input == "1" else code_input
    res = datacollect.get_guba_comments(code, top_n=40)
    #res = ak.stock_hot_rank_em()
    print(res.to_string(col_space=20, index=False, justify='left'))




