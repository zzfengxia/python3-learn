#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-27 21:14
# @desc   : 监控系统的工具包

import psutil, time


def show_cpu():
    # CPU逻辑数量
    print('CPU逻辑数量:', psutil.cpu_count())
    # CPU物理核心
    print('CPU物理核心:', psutil.cpu_count(logical=False))
    # CPU用户/系统/空闲时间
    print('CPU用户/系统/空闲时间:', psutil.cpu_times())
    # 系统启动时间(s)
    print('系统启动时间(s):', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())))
    # CPU使用率
    print('CPU使用率:', psutil.cpu_percent(interval=1, percpu=True))


def show_memory():
    # 内存信息
    print('内存信息:', psutil.virtual_memory())
    # 交换区
    print('交换区:', psutil.swap_memory())


def show_disk():
    # 磁盘IO
    print('磁盘IO:', psutil.disk_io_counters())
    # 磁盘分区
    print('磁盘分区:', psutil.disk_partitions())
    # 磁盘使用
    print('磁盘使用:', psutil.disk_usage("E:"))


def show_network():
    # 网络
    print('网络:', psutil.net_if_addrs())
    # 网络连接
    print('网络连接:', psutil.net_connections())


def show_process():
    # 进程
    psutil.test()
    # psutil.Process()


if __name__ == '__main__':
    # CPU, MEMORY, DISK, NETWORK, PROCESS
    main = 'PROCESS'

    exe = dict(CPU=show_cpu, MEMORY=show_memory, DISK=show_disk, NETWORK=show_network, PROCESS=show_process)

    exe[main].__call__()
