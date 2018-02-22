import sched
import logging
import time
from task import *
from api.HuobiServices import *


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


# 第二个工作函数，自调任务，自己开启定时并启动。
def run_task():
    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    global index
    index = index + 1
    msg = '运行次数（{0}）运行时间 - {1}'.format(index, time.time())
    logging.info(msg)

    buy_order_list = load_buy_order_list()
    for order in buy_order_list:
        # 未执行已经并且已经到达执行时间
        if order.status == OrderStatus.pending.value and order.time < time.time():
            # 买单
            if order.type == OrderType.buy.value :
                # 下单
                result = send_order(order.amount, '', order.symbol, 'buy-limit', order.price)
                order.status = OrderStatus.done.value
                order.id = result["data"]

    save_buy_order_list(buy_order_list)
    s.enter(10, 1, run_task)
    s.run()

logging.info('开始运行 ...')

# 开启自调任务
run_task()


