#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2024-01-24 17:48
@desc   : parse_excel.py
"""

import pandas as pd
import json

if __name__ == '__main__':
    # 指定Excel文件路径
    excel_file_path = 'C:\\Users\\86153\\Desktop\\删除账号.xlsx'

    # 读取Excel文件
    df = pd.read_excel(excel_file_path)

    # 打印数据框的前几行，以查看读取的数据
    #print(df.head())

    # 获取特定列的数据
    # column_data = df['id']
    # id_list = column_data.tolist()
    # print(id_list)
    # 获取特定行和列的数据
    #cell_value = df.at[row_index, 'YourColumnName']

    json_data = []
    # 遍历每一行数据
    for index, row in df.iterrows():
        # 在这里，row是一个包含该行数据的Series对象
        # 你可以通过列名或索引访问每个单元格的值
        #print(f"Index: {index}, Data: {row}")

        # 例如，通过列名访问特定列的值
        id_data = row['id']
        print(id_data)
        ext_data = row['ext_info_params']
        ext_json = json.loads(ext_data)
        tenant_id = ext_json['tenantId']

        res = {'aiAccountId': id_data, 'tenantId': tenant_id}
        json_data.append(res)

        # 或者通过索引访问特定列的值
        #column_value_by_index = row[1]  # 假设 'YourColumnName' 是第二列
        #print(f"Value in the second column: {column_value_by_index}")

    print(f"解析数据条数：{len(json_data)}")
    print(json.dumps(json_data))
