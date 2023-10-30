#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-10-10 18:27
@desc   : 并发测试
"""

import json
import time

import requests

# 定义要请求的URL
url = ''
header = {
    'apiKey': '',
    'apiBase': '',
    'apiType': 'openai'
}
body = {"model_name":"gpt-3.5-turbo","stream":True,"chat_history":[{"role":"assistant","content":"宝马3系的价格会根据选购配置、个人情况等因素而有所不同。具体的价格和优惠情况"},{"role":"assistant","content":"针对微信粉丝有专属优惠哦，可以留个电话哈，给您详细讲解下，不骚扰哈。"},{"role":"human","content":"宝马3系价格多少钱"}],"vehicleBrandIDs":["1","21"]}
def http_request(url, body, header):
    res_data = ""
    response = requests.post(url, headers=header, json=body, stream=True)
    if response.status_code == 200:
        # 遍历响应内容的每个字节块，直接输出到控制台
        # for chunk in response.iter_content(chunk_size=8192):  # 每次读取8192字节
        #     if chunk:
        #         print(chunk)  # 将每个字节块直接打印到控制台
        # 逐行处理流式响应
        for line in response.iter_lines():
            # 解码JSON数据
            decoded_line = line.decode('utf-8')
            # 去除前缀和后缀，得到JSON字符串
            json_string = decoded_line.replace('data: ', '').rstrip()
            if not json_string:
                continue
            # 尝试解析JSON数据
            try:
                json_data = json.loads(json_string)
                # 获取JSON中的属性
                desired_property = json_data['data']
                res_data = res_data + desired_property
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON: {e}, {json_string}')
    else:
        print('请求失败。')
    print(f'res json:{res_data}')

if __name__ == '__main__':
    start_time = time.time()
    http_request(url, body, header)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    # 打印耗时
    print(f'代码执行耗时：{elapsed_time:.2f} 毫秒')
