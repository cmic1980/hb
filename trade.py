import sched
import time
from api.HuobiServices import *
import pymysql

# 计数器，一个循环任务，总共让自己执行3次
index = 0

def run_task():
    global index
    index = index + 1

    # 查询现有数量
    balance = get_symbol_balance('omg')


    print("now is", time.time())
    print("balance", balance)

    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, run_task)
    s.run()

run_task()