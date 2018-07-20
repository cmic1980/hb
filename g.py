import datetime
import json
import time
import sched
import pymysql.cursors
from api.HuobiServices import *


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='hb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_order_list_by_status(status):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select *, CONVERT_TZ(buy_time,'+00:00','+8:00') as r_buy_time from order_item where status=%s"
            cursor.execute(sql, (status))
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            return data;
        # your changes.
        connection.commit()
    finally:
        connection.close()


# 下单后更新状态
def set_buy_order(order):
    symbol = order["symbol"]
    print("set buy order 1: ", symbol)

    now = datetime.datetime.now()
    buy_time = order["r_buy_time"]
    if now > buy_time:
        print("set buy order 2: ", symbol)

        connection = connection = get_connection()
        try:
            with connection.cursor() as cursor:
                # 下单
                symbol = order["symbol"]
                amount = order["amount"]
                buy_price = 0
                kline_list = get_kline_ex(symbol, "60min", 30)
                for kline in kline_list:
                    kline_time = kline["time"]
                    if buy_time == kline_time:
                        open = kline["open"]
                        buy_price = open
                        sell_price = (1 + 1.8 / 100) * buy_price

                result = send_order(amount, '', symbol, 'buy-limit', buy_price)

                sql = "update order_item set status=2,order_id=%s,buy_price=%s,sell_price=%s where order_item_id=%s"
                order_id = result["data"]
                order_item_id = order["order_item_id"]
                cursor.execute(sql, (order_id, buy_price,sell_price,order_item_id))

                print("update order status: ", order_item_id)
            connection.commit()
        finally:
            connection.close()


# 更新完全成交买单状态
def update_buy_order_complete(order):
    order_id = order["order_id"]
    symbol = order["symbol"]
    print("update buy order complete 1: ", symbol)

    if order_id != -1:
        print("update buy order complete 2: ", symbol)
        order = order_info(order_id)
        state = order["data"]["state"]
        if state == "filled":
            connection = connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    sql = "update order_item set status=3 where order_item_id=%s"
                    order_item_id = order["order_item_id"]
                    cursor.execute(sql, (order_item_id))
                connection.commit()
            finally:
                connection.close()


# 下单一小时如果不成交撤单
def cancel_buy_order(order):
    now = datetime.datetime.now()
    buy_time = order["r_buy_time"]
    symbol = order["symbol"]
    print("cancel buy order 1: ", symbol)
    buy_time = buy_time + datetime.timedelta(hours=1)
    if now > buy_time:
        print("cancel buy order 2: ", symbol)
        order_id = order["order_id"]
        if order_id != -1:
            cancel_order(order_id)

            connection = connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    sql = "update order_item set status=4 where order_item_id=%s"
                    order_item_id = order["order_item_id"]
                    cursor.execute(sql, (order_item_id))
                connection.commit()
            finally:
                connection.close()


# 下卖单
def set_sell_order(order):
    order_id = order["order_id"]
    sell_price = order["sell_price"]
    symbol = order["symbol"]
    print("set_sell_order 1: ", symbol)
    if order_id != -1:
        symbol = order["symbol"]
        print("set_sell_order 2: ", symbol)
        balance = get_symbol_balance(symbol.replace("eth",""))
        # 如果余额大于0.01，挂卖单
        if balance>0.01:
            result = send_order(balance, '', symbol, 'sell-limit', sell_price)
            pass

        # 完成的买单/取消的买单 下完买单后变为完成状态
        status = order["status"]
        if status==3 or status==4:
            connection = connection = get_connection()
            try:
                with connection.cursor() as cursor:
                    sql = "update order_item set status=5 where order_item_id=%s"
                    order_item_id = order["order_item_id"]
                    cursor.execute(sql, (order_item_id))
                connection.commit()
            finally:
                connection.close()

# 计数器，一个循环任务，总共让自己执行3次
def run_task():
    # 打印信息
    # 下买单
    order_list = get_order_list_by_status(1);
    for order in order_list:
        set_buy_order(order)

    # 更新完全成交买单状态 状态 -> 3
    order_list = get_order_list_by_status(2);
    for order in order_list:
        update_buy_order_complete(order)

    # 取消买单 状态 -> 4
    order_list = get_order_list_by_status(2);
    for order in order_list:
        cancel_buy_order(order)

    # 下卖单 完成的买单/取消的买单/挂的买单都有可能部分成交
    order_list2 = get_order_list_by_status(2);
    order_list3 = get_order_list_by_status(3);
    order_list4 = get_order_list_by_status(4);

    order_list = [];
    if len(order_list2) != 0:
        order_list = order_list + order_list2;
    if len(order_list3) != 0:
        order_list = order_list + order_list3;
    if len(order_list4) != 0:
        order_list = order_list + order_list4;

    for order in order_list:
        set_sell_order(order)

    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, run_task)
    s.run()


run_task();
