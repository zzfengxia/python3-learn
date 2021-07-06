#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-06-30 15:25
# @desc   : 创建线程池

from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import os, time, random


def call_func(name):
    print('Run task %s (%s)...' % (name, os.getpid()))

# 调用cmd命令的任务函数
def call_api(filename):
    cmd_str = f'Call xx.exe -o {filename} -r "xx.py"'
    print(cmd_str)
    time.sleep(2)


if __name__ == '__main__':
    # 创建线程池
    # p = Pool(4)
    # for i in range(5):
    #     p.apply_async(call_func, args=(i,))
    # p.close()
    # p.join()
    # print('All subprocesses done.')
    #
    # # 调用cmd命令
    # port = 443
    # ipconfig = os.popen(f"netstat -ant|findstr :{port}")
    # info = ipconfig.readlines()
    # for line in info:  # 按行遍历
    #     line = line.strip('\r\n')
    #     print(line)
    #
    # exe = "D://cam.exe"
    # file = "x.qjp"
    # cmd = f'Call {exe} -o "{file}" -r "x.py"'
    # print(cmd)

    # 开启线程池，参数可以指定线程的数量
    pool = ThreadPoolExecutor(5)

    # 遍历文件目录
    g = os.walk('D:\python_code\config1')

    for i in range(10):
        pool.submit(call_api, i)

    # wait 为 True时会等待所有的任务完成才会返回
    pool.shutdown(wait=True)

    print("执行完成...")

