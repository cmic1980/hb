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
    task_list = get_task_list()

    print("now is", time.time())
    print("balance", balance)

    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, run_task)
    s.run()


def get_task_list():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "password", "hb")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select * from daily_trade")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    list = []
    for row in data:
        daily_trade = DailyTrade(row)
        list.append(daily_trade)
    # 关闭数据库连接
    db.close()

    return list

# 日常交易任务
class DailyTrade(object):
    def __init__(self,row):
        self.id = row[0]
        self.balance = row[1]
        self.symbol = row[2]
        self.exec_time = row[3]
        self.t = row[4]
        self.buy_order_id = row[5]
        self.buy_price = row[6]
        self.sell_order_id = row[7]
        self.status = row[7]

run_task()