#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2021-06-27
# @desc   : 比对两个同名文件内容是否相同

import filecmp
import sys
import os
import argparse

# 读取文件
def read_file(file_name):
    try:
        file_desc = open(file_name, 'r')
        text = file_desc.read().splitlines()
        file_desc.close()
        return text
    except IOError as error:
        print('文件读取错误:', error)
        sys.exit()


# 比较两个文件并把结果生成一份txt文本
# def compare_file(file1, file2):
#     if file1 == "" or file2 == "":
#         print('文件路径不能为空。文件1:%s, 文件2: %s' % (file1, file2))
#         sys.exit()
#
#     print('%s VS %s, 文件比对开始...' % (file1, file2))
#     text1_lines = read_file(file1)
#     text2_lines = read_file(file2)
#     diff = difflib.HtmlDiff()
#     result = diff.make_file(text1_lines, text2_lines)
#     try:
#         with open('result_comparation.html', 'w') as result_file:
#             result_file.write(result)
#     except IOError as error:
#         print('写入输出文件错误: ', error)

def findAllFile(dir):
    fl = []
    g = os.walk(dir)
    for root, ds, fs in g:
        for f in fs:
            #fl.append(os.path.join(root, f))
            fl.append(f)
    return fl


if __name__ == "__main__":
    # 文件目录
    #file_dir1 = 'D:\python_code\config1'
    #file_dir2 = 'D:\python_code\config2'
    # outfile = 'D:\python_code\com_result.txt'
    # 读取命令行参数
    arg_list = sys.argv
    if len(arg_list) < 4:
        print(f'非法参数，需要至少两个目录参数和一个结果输出目录参数')
        exit(-1)
    # 文件目录
    file_dir1 = arg_list[1]
    file_dir2 = arg_list[2]

    list_file = findAllFile(file_dir1)
    print(list_file)
    match, mismatch, errors = filecmp.cmpfiles(file_dir1, file_dir2, list_file)

    with open(arg_list[3], 'w') as f:
        f.write(f'基准文件目录: {file_dir1}\n')
        for match_file in match:
            f.write(f'{match_file:<{100}}:  true \n')
        for mis_file in mismatch:
            f.write(f'{mis_file:<{100}}:  false \n')
        for erro_file in errors:
            f.write(f'{erro_file:<{100}}:  无同名文件或比对失败 \n')

