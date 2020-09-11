#!/usr/bin/env python3
# *_*coding=utf-8
# @author : Francis.zz
# @date   : 2018-06-02 21:18
# @desc   : 分布式进程-任务分发器

import queue
import random
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


# windows下运行
def return_task_queue():
    global task_queue
    return task_queue  # 返回发送任务队列


def return_result_queue():
    global result_queue
    return result_queue # 返回接收结果队列


class QueueManage(BaseManager):
    pass


if __name__ == '__main__':
    # 注册队列到网络上
    QueueManage.register('get_task_queue', callable=return_task_queue)
    QueueManage.register('get_result_queue', callable=return_result_queue)
    # 发布端口
    manager = QueueManage(address=('127.0.0.1', 6000), authkey=b'123')
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)
    # 关闭:
    manager.shutdown()
    print('master exit.')
