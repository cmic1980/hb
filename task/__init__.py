# __init__.py
import json
import datetime
from enum import Enum


class OrderType(Enum):
    buy = 1
    sell = 2

class OrderStatus(Enum):
    pending = 1
    done = 2
    cancelled = 3

class BuyOrder():
    def __init__(self):
        self.symbol = None
        self.amount = 0
        self.time = None
        self.id = ""
        self.status = OrderStatus.pending  # 1 pending, 2 done
        self.type = OrderType.buy
        self.price = 0
        self.cancel_time = None


def load_buy_order_list():
    # 读取下单Order任务
    file = open("task/buy.json")
    s = file.read()
    file.close()

    item_list = json.loads(s)

    # 转换成 Order List 对象
    order_list = []
    for item in item_list:
        order = BuyOrder()
        order.symbol = item["symbol"]
        order.amount = item["amount"]
        order.time =  item["time"]
        order.status = int(item["status"])
        order.type = int(item["type"])
        order.price = float(item["price"])
        if item.__contains__("cancel_time") == True:
            order.cancel_time = item["cancel_time"]
        order_list.append(order)

    return order_list

def save_buy_order_list(order_list):
    pending_list = []

    # 读取完成 的订单
    now = datetime.datetime.now()
    file = open("task/out.json")
    s = file.read()
    file.close()

    done_list = []
    if s !="":
        done_list = json.loads(s)


    for order in order_list:
        item = {};
        item["id"] = order.id
        item["symbol"] = order.symbol
        item["amount"] = order.amount
        item["time"] = order.time
        item["status"] = order.status
        item["type"] = order.type
        item["price"] = order.price
        if order.status == OrderStatus.pending.value:
            pending_list.append(item)

        if order.status == OrderStatus.done.value:
            done_list.append(item)

    # 保存 未完成 的订单
    s = json.dumps(pending_list)
    file = open("task/buy.json", 'w')
    file.write(s)
    file.close()

    # 保存 完成 的订单
    s = json.dumps(done_list)
    now = datetime.datetime.now()
    file = open("task/out.json", "w")
    file.write(s)
    file.close()