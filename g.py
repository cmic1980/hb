import json
import time
import sched
import pymysql.cursors


def get_current_order_list():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='hb',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select * from order_item where status=1"
            cursor.execute(sql)
            # 使用 fetchone() 方法获取一条数据
            data = cursor.fetchall()
            return data;
        # your changes.
        connection.commit()
    finally:
        connection.close()


# 下单后更新状态
def update_order_status(order):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='hb',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "update order_item set status=2 where order_item_id=%s"
            order_id = order["order_item_id"]
            cursor.execute(sql, (order_id))

            print("update order status: ", order_id)
        connection.commit()
    finally:
        connection.close()

# 计数器，一个循环任务，总共让自己执行3次
def run_task():

    # 打印信息
    print("run time is ", time.time())
    order_list = get_current_order_list();

    print("current order list: ", len(order_list))

    for order in order_list:
        update_order_status(order)


    # 只要没有让自己调用到第3次，那么继续重头开始执行本任务
    # 这里的delay 可以重新指定
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 0, run_task)
    s.run()


run_task();
