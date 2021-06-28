#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2021-06-27
# @desc   : 比对两个同名文件内容是否相同

import filecmp
import sys
import os
import difflib
import argparse


# 读取文件
def read_file(file_name, encoding='uft-8'):
    try:
        with open(file_name, 'r', encoding=encoding) as file_desc:
            text = file_desc.read().splitlines()
            return text
    except IOError as error:
        print('文件读取错误:', error)


# 比较两个文件并把结果生成一份html文件
def compare_file_to_html(file1, file2):
    if file1 == "" or file2 == "":
        print('文件路径不能为空。文件1:%s, 文件2: %s' % (file1, file2))
        sys.exit()

    print('%s VS %s, 文件比对开始...' % (file1, file2))
    text1_lines = read_file(file1)
    text2_lines = read_file(file2)
    diff = difflib.HtmlDiff()
    result = diff.make_file(text1_lines[2:], text2_lines[2:])
    try:
        with open('F:\\result_comparation.html', 'w') as result_file:
            result_file.write(result)
    except IOError as error:
        print('写入输出文件错误: ', error)


def compare_file(file1, file2, skip_line=0, encoding='utf-8'):
    if file1 == "" and file2 == "":
        raise Exception('file path is not allow null')

    text1_lines = read_file(file1, encoding)
    text2_lines = read_file(file2, encoding)
    skip_line_min = min(len(text1_lines), len(text2_lines), int(skip_line))
    diff_result = difflib.ndiff(text1_lines[skip_line_min:], text2_lines[skip_line_min:])

    for res_line in diff_result:
        if res_line[0:1] == '+' or res_line[0:1] == '-':
            return False
    return True


def findAllFile(dir):
    fl = []
    g = os.walk(dir)
    for root, ds, fs in g:
        for f in fs:
            # fl.append(os.path.join(root, f))
            fl.append(f)
    return fl


def cmp_file_whith_skip_line(dir1, dir2, list_file, skip_line=0, encoding='utf-8'):
    # match, mismatch, errors
    res = ([], [], [])

    for x in list_file:
        ax = os.path.join(dir1, x)
        bx = os.path.join(dir2, x)

        if not os.path.exists(bx):
            res[2].append(x)
            continue
        try:
            if compare_file(ax, bx, skip_line, encoding):
                res[0].append(x)
            else:
                res[1].append(x)
        except:
            res[2].append(x)

    return res


if __name__ == "__main__":
    # 读取命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store_true', default=False,
                        help='快速比对模式')
    parser.add_argument('-s', action='store_true', default=False,
                        help='比对行模式，可指定跳过的行数')
    parser.add_argument('--dir1')
    parser.add_argument('--dir2')
    parser.add_argument('--out_file', help='比对结果输出文件')
    parser.add_argument('--skip_line', required=False, help='跳过的行数')
    parser.add_argument('--encoding', required=False, help='文件编码，比对行模式需要指定，默认UTF-8')
    options = parser.parse_args()

    if not options.dir1:
        print(f'args "dir1" is must')
        exit(-1)
    if not options.dir2:
        print(f'args "dir2" is must')
        exit(-1)
    if not options.out_file:
        print(f'args "out_file" is must')
        exit(-1)

    file_dir1 = options.dir1
    file_dir2 = options.dir2
    out_file = options.out_file

    list_file = findAllFile(file_dir1)
    match, mismatch, errors = ([], [], [])
    print('开始比对...')
    if options.f:
        match, mismatch, errors = filecmp.cmpfiles(file_dir1, file_dir2, list_file)
    elif options.s:
        skip_line = options.skip_line or 0
        encoding = options.encoding or 'UTF-8'
        match, mismatch, errors = cmp_file_whith_skip_line(file_dir1, file_dir2, list_file, skip_line, encoding)
    else:
        print(f'请指定比对模式, -f or -s')
        exit(-1)
    with open(out_file, 'w') as f:
        f.write(f'基准文件目录: {file_dir1}\n')
        for match_file in match:
            f.write(f'{match_file:<{100}}:  true \n')
        for mis_file in mismatch:
            f.write(f'{mis_file:<{100}}:  false \n')
        for erro_file in errors:
            f.write(f'{erro_file:<{100}}:  无同名文件或比对失败 \n')
    print(f'比对结束，结果已输出至 {out_file} 文件')
    exit(0)
