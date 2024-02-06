#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2024-01-18 22:44
@desc   : parse_json.py
"""

import json

if __name__ == '__main__':
    file_content = None
    with open('C:\\Users\\86153\\Desktop\\response_1705588832131.json', 'r', encoding='utf-8') as file:
        file_content = file.read()

    if file_content is not None:
        try:
            json_data = json.loads(file_content)
            data_list = json_data.get('data')
            print(f'解析数据条数：{len(data_list)}')
            account_list = []
            for data in data_list:
                account_list.append(data.get('aiAccountId'))
            print(f'成功解析:{len(account_list)}')
            print(f'({", ".join(map(str, account_list))})')
        except json.JSONDecodeError as e:
            print(f"解析JSON时发生错误: {e}")
