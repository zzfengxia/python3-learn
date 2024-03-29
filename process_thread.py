#!/usr/bin/env python3
# coding: utf-8

"""进程与线程"""

__author__ = 'Francis.zz'

import os, time, random, subprocess
from threading import Thread, Lock
from multiprocessing import Process, Pool, Queue
from concurrent.futures import ThreadPoolExecutor

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


balance = 0


def write_fun():
    global balance
    lock = Lock()
    for i in range(1000):
        # 同步锁
        lock.acquire()
        try:
            balance += 1
            # balance -= 1
        finally:
            lock.release()


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

    
# 调用cmd命令的任务函数
def call_api(filename):
    cmd_str = f'Call xx.exe -o {filename} -r "xx.py"'
    print(cmd_str)
    time.sleep(2)

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

        # 进程会拷贝一份数据到自己内存,只能用Queue,Pipes同步数据
        pp1 = Process(target=write_fun)
        pp2 = Process(target=write_fun)
        pp1.start()
        pp2.start()

        pp1.join()
        pp2.join()
        print('最终结果:', balance)

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

    elif unit == 'THREAD':
        # 线程之间可以共享数据。CPython解释器使用了GIL导致多线程只能在一个CPU内执行
        t1 = Thread(target=write_fun, name='t1')
        t2 = Thread(target=write_fun, name='t2')
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('最终结果:', balance)
     
    # 开启线程池，参数可以指定线程的数量
    pool = ThreadPoolExecutor(5)

    # 遍历文件目录
    g = os.walk('D:\python_code\config1')
    for root, ds, fs in g:
        for f in fs:
            # 遍历文件
            full_path = os.path.join(root, f)
            pool.submit(call_api, full_path)

    pool.shutdown(wait=True)
