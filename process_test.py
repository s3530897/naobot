# -*- coding: utf-8 -*
import time
from multiprocessing import Process
from swift_turnon import turnsw
import os

#线程测试
global t
t=turnsw()
def f(name):
    print('hello', name)
    print('我是子进程')
    t.swiftturn()
    time.sleep(10)
    print('我是子进程')
    t.swiftturn()
    time.sleep(10)
    print('我是子进程')
    time.sleep(10)
    print('我是子进程')

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    t.swiftturn()
    time.sleep(1)
    print('执行主进程的内容了')
    time.sleep(12)
    t.swiftturn()
    print('停止吧子进程')
    p.terminate()
    time.sleep(3)
    t.swiftturn()
    print('233')
    time.sleep(3)
    p.start()
    time.sleep(12)