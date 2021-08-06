#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-07-06 14:37
# @desc   : 检测windows进程是否崩溃

import sys
import subprocess
import concurrent.futures
import time


def check_crash2():
    subprocess_flags = 0
    print(0x8000000)
    # windows禁用弹窗
    if sys.platform.startswith("win"):
        import ctypes

        SEM_FAILCRITICALERRORS = 0x0001
        SEM_NOGPFAULTERRORBOX = 0x0002  # From MSDN
        print(ctypes.windll.kernel32)
        # 设置windows不显示错误报告对话框。这里如果解决不了的话，只能通过修改注册表禁用windows错误弹窗UI
        ctypes.windll.kernel32.SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX)
        print(ctypes.windll.kernel32)
        subprocess_flags = 0x8000000  # subprocess.CREATE_NO_WINDOW

    # process = subprocess.Popen('D:\\java_dev\\apache-jmeter-5.2.1\\bin\\jmeter.bat',
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.STDOUT,
    #                            shell=True,
    #                            universal_newlines=True,
    #                            creationflags=subprocess_flags)
    process = subprocess.Popen('D:\\java_dev\\apache-jmeter-5.2.1\\bin\\jmeter.bat1',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess_flags)
    print(f'进程号:{process.pid}')

    (stdout, stderr) = process.communicate()
    # ret_code = process.poll()

    # 0表示正常返回
    print(f'进程返回码：{process.returncode}, error: {stderr}')


def check_crash(f_name, subp_flags, tout=10):
    """
    检查程序执行的方法

    :return 运行结果int，9:超时  0:正常  -1:崩溃
    """
    cmd = 'ping baidu.com -t'
    if f_name % 2 == 0:
        cmd = 'ipconfig'
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subp_flags)
    try:
        (stdout, stderr) = process.communicate(timeout=tout)
        if process.returncode == 0:
            return 0
        else:
            return -1
    except subprocess.TimeoutExpired as te:
        # 超时需要杀掉进程，不然会无限创建超时的进程
        process.kill()
        return 9


if __name__ == '__main__':
    subprocess_flags = 0
    # windows禁用弹窗
    if sys.platform.startswith("win"):
        import ctypes

        SEM_FAILCRITICALERRORS = 0x0001
        SEM_NOGPFAULTERRORBOX = 0x0002  # From MSDN
        print(ctypes.windll.kernel32)
        # 设置windows不显示错误报告对话框。这里如果解决不了的话，只能通过修改注册表禁用windows错误弹窗UI
        ctypes.windll.kernel32.SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX)
        subprocess_flags = 0x8000000

    fs_dict = {}
    # max_workers设置最大允许启动的进程数量
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=5)
    # 遍历文件
    for i in range(10):
        fs = executor.submit(check_crash, i, subprocess_flags, 2)
        # 异步结果存入dict，key为文件名，value为Future异步结果
        fs_dict[i] = fs

    # 遍历异步Future结果
    while True:
        if len(fs_dict) == 0:
            break
        for key in list(fs_dict.keys()):
            sync_res = fs_dict.get(key)
            if sync_res is None:
                del fs_dict[key]
                continue
            try:
                check_code = sync_res.result(timeout=0)
                if check_code is not None:
                    print(f'文件:{key} 执行结果：{check_code}')
                    del fs_dict[key]
            except concurrent.futures.TimeoutError:
                continue
            except concurrent.futures.process.BrokenProcessPool as bpe:
                print("崩溃")
            except Exception as e:
                print('任务执行异常:', e)
                del fs_dict[key]


    # 调用shutdown会阻塞，直到所有任务执行完成，所有不能提前
    executor.shutdown()
    print("结束")
