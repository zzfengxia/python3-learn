#!/usr/bin/env python3
# coding: utf-8

"""进程与线程"""

__author__ = 'Francis.zz'

import os, time, random, subprocess
from multiprocessing import Process, Pool, Queue


def proc_run(name):
    print('child process %s (%s)' % (name, os.getpid()))


def proc_task(name):
    print('running task %s (%s)' % (name, os.getpid()))
    start = time.time()
    # 休眠
    time.sleep(random.random() * 2)
    end = time.time()
    print('task %s run %s s' % (name, (end - start)))


# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())


# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


def ping_exe(host):
    # 创建子进程，并控制其输入输出
    print('$ ping', host)
    # 中文乱码
    # r = subprocess.call(['ping', 'baidu.com'], **dict(encoding='gbk'))
    # print('Exit code:', r)

    subp = subprocess.Popen(['ping', host], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # 解决中文乱码问题
    # subp.wait()
    # print(subp.stdout.read().decode('gbk'))

    # 按行输出(实时输出)
    flag = False
    while not flag:
        line = subp.stdout.readline()
        if line:
            print(line.decode('gbk'))
        else:
            flag = True
    print('Exit code:', subp.returncode)


if __name__ == '__main__':
    # MULTI_PROCESS, SUB_PROCESS, PROCESS_COMMUNICATE
    unit = 'SUB_PROCESS'

    if unit == 'MULTI_PROCESS':
        print('CPU数量:', os.cpu_count())
        print('当前PID:', os.getpid())
        # Only works on Unix/Linux/Mac,fork调用一次，返回两次，子进程总是返回0，父进程返回子进程pid
        # pid = os.fork()
        # if pid == 0:
        #     print('当前为子进程:%s，父进程ID:%s' % (os.getpid(), os.getppid()))
        # else:
        #     print('当前为父进程:%s, 创建的子进程ID:%s' % (os.getpid(), pid))

        # 创建进程,target参数为run的方法，args为参数元组
        p1 = Process(target=proc_run, args=('c1',))
        p2 = Process()
        # 启动子进程
        p1.start()
        # 等待子进程结束
        p1.join()
        print('current pid:%s,child process end.' % os.getpid())

        # 进程池创建进程
        pool = Pool(3)
        for i in range(4):
            # 异步调用
            pool.apply_async(proc_task, args=(i,))

        # 先关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()
        print("all sub process done")

    elif unit == 'SUB_PROCESS':
        ping_exe('baidu.com')

        print('\n$ nslookup')
        p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 输入参数，或者使用stdin输入
        output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
        print(output.decode('gbk'))
        print('Exit code:', p.returncode)

    elif unit == 'PROCESS_COMMUNICATE':
        # 进程间通信，使用Queue、Pipes
        queue = Queue()
        wp = Process(target=write, args=(queue,))
        rp = Process(target=read, args=(queue,))

        wp.start()
        rp.start()

        wp.join()
        rp.terminate()

        print('process done.')
