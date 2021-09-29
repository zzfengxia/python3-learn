# -*- coding: UTF-8 -*-
# !/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-09-28 10:24
# @desc   :

import socket
import logging
import os
import datetime
import concurrent.futures, subprocess
import time


class LoggerTest(object):

    def __init__(self, loggername):
        # python官方文档中提供的一段示例，使用logging模块产生logger对象
        logging.basicConfig(datefmt='%Y-%m-%d%I:%M:%S %p')
        # 创建一个日志对象，这个参数可以随便填，这个参数唯一标识了这个日志对象
        self.logger = logging.getLogger(loggername)
        # 设置级别
        self.logger.setLevel(logging.INFO)

        current_path = os.path.dirname(os.path.realpath(__file__))
        # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把log变成文件名的一部分了
        log_path = current_path + "/log/"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # 指定输出的日志文件名
        now = datetime.datetime.now()
        dt = now.strftime('%Y-%m-%d')
        # 日志的文件名
        logname = log_path + str(loggername) + '.' + str(dt) + '.log'
        # 创建一个handler，用于写入日志文件, 'a'表示追加
        file_handler = logging.FileHandler(logname, 'a')
        # 为logger添加的日志处理器
        self.logger.addHandler(file_handler)

        formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s - %(message)s')
        # 设置日志内容的格式
        file_handler.setFormatter(formatter)


def get_ip_by_host(host):
    if host == '':
        return None
    ip_arr = []
    try:
        ip_arr = socket.gethostbyname_ex(host)
        return ip_arr
    except Exception as e:
        logger = LoggerTest('get_ip_by_host')
        logger.logger.error(f'parse ip failed by host {host}')


def ping_check(ip):
    logger = LoggerTest('ping')
    cmd = f'ping {ip} -c 30'
    ping = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
    # 实时输出
    while ping.poll() is None:
        line = ping.stdout.readline()
        logger.logger.info(line.decode('gbk'))


def list_ping_host(host):
    logger = LoggerTest('ping')
    parse_res = get_ip_by_host(host)
    ip_arr = parse_res[len(parse_res) - 1]
    logger.logger.info(f'************* current ip list:{ip_arr}')

    worker_size = int(len(ip_arr) / 2 + 1)
    executor = concurrent.futures.ProcessPoolExecutor(worker_size)
    for ip in ip_arr:
        executor.submit(ping_check, ip)

    executor.shutdown(wait=True)
    logger.logger.info('\n\n\n')


if __name__ == '__main__':
    host = 'gateway.95516.com'
    while True:
        list_ping_host(host)
        time.sleep(10)
