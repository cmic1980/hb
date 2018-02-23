import sched
import logging
import time
from task import *
from api.HuobiServices import *
import math


def intitial_logging():
    ''''' Output log to file and console '''
    # Define a Handler and set a format which output to file
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename='log.txt',  # log文件名
        filemode='w')  # 写入模式“w”或“a”
    # Define a Handler and set a format which output to console
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.INFO)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)  # 实例化添加handler


if __name__ == "__main__":
    intitial_logging()

s = sched.scheduler(time.time, time.sleep)
# 计数器，一个循环任务，总共让自己执行3次
index = 0

cancel_list = []


# 第二个工作函数，自调任务，自己开启定时并启动。
def run_task():
    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    global index
    index = index + 1
    # msg = '运行次数（{0}）运行时间 - {1}'.format(index, time.time())
    # logging.info(msg)

    # 下买单
    buy_order_list = load_buy_order_list()
    for order in buy_order_list:
        # 未执行已经并且已经到达执行时间
        if order.status == OrderStatus.pending.value and order.time < time.time():
            type_name = '下买单'
            order_type = ''
            amount = order.amount

            if order.type == OrderType.buy.value:
                order_type = 'buy-limit'
                type_name = '下买单'
                # 加入买单 cancel 任务
                if order.cancel_time != None:
                    cancel = {"id": order.id, "time": order.cancel_time}
                    cancel_list.append(cancel)

            elif order.type == OrderType.sell.value:
                order_type = 'sell-limit'
                type_name = '下卖单'

                currency = order.symbol.replace('eth', '').replace('btc', '')
                balance = get_symbol_balance(currency)
                amount = float(balance['balance'])
                amount = round(amount, 2)

            # 下单
            result = send_order(amount, '', order.symbol, order_type, order.price)
            # 设置状态
            if result["status"] == "ok":
                order.id = result["data"]
                if order.type == OrderType.buy.value:
                    order.status = OrderStatus.done.value
                elif order.type == OrderType.sell.value:  # 处理卖单
                    if order.status == OrderStatus.pending.value and order.cancel_time < time.time():
                        order.status = OrderStatus.done.value

            msg = "{0}（ID：{1}，交易品种：{2}， 数量：{3}，时间：{4}，价格：{5}）".format(type_name, order.id, order.symbol, amount,
                                                                      order.time, order.price)
            logging.info(msg)

    save_buy_order_list(buy_order_list)

    # 取消买单
    for order in cancel_list:
        # 未执行已经并且已经到达执行时间
        if order["time"] < time.time():
            cancel_order(order["id"])
            pass

    s.enter(10, 1, run_task)
    s.run()


logging.info('开始运行 ...')

# 开启自调任务
run_task()
