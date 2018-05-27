import datetime
import json
import time
import sched
import pymysql.cursors
from api.HuobiServices import *

def get_order_list_by_status(status):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='hb',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select *, CONVERT_TZ(buy_time,'+00:00','+8:00') as r_buy_time from order_item where status=%s"
            cursor.execute(sql,(status))
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            return data;
        # your changes.
        connection.commit()
    finally:
        connection.close()




# 下单后更新状态
def set_buy_order(order):
    now = datetime.datetime.now()
    buy_time = order["r_buy_time"]

    if now > buy_time:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='password',
                                     db='hb',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # 下单
                symbol = order["symbol"]
                amount = order["amount"]
                order_type = 'buy-limit'
                price = 0
                kline_list = get_kline_ex(symbol, "60min", 30)
                for kline in kline_list:
                    kline_time = kline["time"]
                    if buy_time == kline_time:
                        open = kline["open"]
                        price = open

                result = send_order(amount, '', symbol, order_type, price)

                sql = "update order_item set status=2,order_id=%s where order_item_id=%s"
                order_id = result["data"]
                order_item_id = order["order_item_id"]
                cursor.execute(sql, (order_id,order_item_id))

                print("update order status: ", order_item_id)
            connection.commit()
        finally:
            connection.close()

# 下单一小时如果不成交撤单
def cancel_buy_order(order):
    now = datetime.datetime.now()
    buy_time = order["r_buy_time"]
    buy_time = buy_time + datetime.timedelta(hours=1)
    if now > buy_time:
        order_id = order["order_id"]
        if order_id!=-1:
            cancel_order(order_id)
# 下卖单
def set_sell_order(order):
    # 有
    symbol = order["symbol"]
    l1 = orders_list(symbol, "submitted",'buy-limit')
    pass

# 计数器，一个循环任务，总共让自己执行3次
def run_task():
    # 打印信息
    print("run time is ", time.time())

    # 下买单
    order_list = get_order_list_by_status(1);
    print("current order list: ", len(order_list))
    for order in order_list:
        set_buy_order(order)

    # 下卖单
    order_list = get_order_list_by_status(2);
    for order in order_list:
        cancel_buy_order(order)

    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, run_task)
    s.run()


run_task();
