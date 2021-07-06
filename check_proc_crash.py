#!/usr/bin/env python3
# coding  : utf-8
# @author : Francis.zz
# @date   : 2021-07-06 14:37
# @desc   : 检测windows进程是否崩溃

import sys
import subprocess

if __name__ == '__main__':
    subprocess_flags = 0
    # windows禁用弹窗
    if sys.platform.startswith("win"):
        import ctypes

        SEM_NOGPFAULTERRORBOX = 0x0002  # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)
        subprocess_flags = 0x8000000 #subprocess.CREATE_NO_WINDOW

    # process = subprocess.Popen('D:\\java_dev\\apache-jmeter-5.2.1\\bin\\jmeter.bat',
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.STDOUT,
    #                            shell=True,
    #                            universal_newlines=True,
    #                            creationflags=subprocess_flags)
    process = subprocess.Popen('D:\\java_dev\\apache-jmeter-5.2.1\\bin\\jmeter.bat',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess_flags)
    print(f'进程号:{process.pid}')

    (stdout, stderr) = process.communicate()
    # ret_code = process.poll()

    # 0表示正常返回
    print(f'进程返回码：{process.returncode}, error: {stderr}')
