import pymysql.cursors
from api.HuobiServices import *
from datetime import datetime

'''
symbol_list = get_eth_symbol_list()
for symbol in symbol_list:
    kline_list = get_kline_ex(symbol,"60min",2000)
    print(symbol)
    print(kline_list)
'''


def show_analysis_table(kline_list, hour, t):
    list = []
    item = None
    for kline in kline_list:
        time = kline["time"]
        if time.hour == hour:
            item = {}
            item["time"] = kline["time"]
            item["open"] = kline["open"]
            item['high'] = kline["high"]
            item['ht'] = kline["time"]
            list.append(item)
            # item["high"] = kline["high"]

        if item != None:
            item['close'] = kline["close"]
            if item['high'] < kline["high"]:
                item['high'] = kline["high"]
                item['ht'] = kline["time"]

    # 正收益
    c1 = 0
    # 负收益
    c2 = 0
    d = 100
    price = 0
    for item in list:
        if item['open'] != 0:
            price = item['open']
            s = (item['high'] - item['open']) * 100 / item['open']

            if s > t:
                c1 = c1 + 1
                d = d * (1 + t / 100)
            else:
                c2 = c2 + 1
                s2 = (item['close'] - item['open']) / item['open']
                d = d * (1 + s2)

    out = {}
    out["hour"] = hour
    out["t"] = t
    out["income"] = d
    out["price"] = price
    out["scale"] = c1 / (c1 + c2)

    return out


def get_symbol_analysis(symbol, probability, show_detail=False):
    kline_list = get_kline_ex(symbol, "60min", 2000)
    symbol_analysis = {}

    # 48小时 成交量， 为了找到投资成交量比较大币种
    # amount - 当前币种成交量， vol - ETH 成交量
    amount_list = []
    vol_list = []

    kline_length = len(kline_list)
    for i in range(0, 48):
        index = kline_length - 1 - i
        if index < 0:
            break
        kline = kline_list[index]
        kline_amount = kline['amount']
        kline_vol = kline['vol']

        amount_list.append(kline_amount)
        vol_list.append(kline_vol)

    amount48 = 0
    for amount in amount_list:
        amount48 = amount48 + amount
    symbol_analysis["amount"] = amount48 / len(amount_list)

    vol48 = 0
    for vol in vol_list:
        vol48 = vol48 + vol
    symbol_analysis["vol"] = vol48 / len(vol_list)


    # 分析
    max_income = 0
    max_out = 0
    for i in range(0, 24):
        for j in range(10, 60):
            out = show_analysis_table(kline_list, i, 0.1 * j)
            if out["income"] > max_income and out["scale"] > probability:
                max_income = out["income"]
                max_out = out
            if show_detail:
                print(out)

    symbol_analysis["symbol"] = symbol
    symbol_analysis["max_out"] = max_out
    symbol_analysis["days"] = len(kline_list)
    return symbol_analysis


def submit_analysis_result(analysis_time, symbol_analysis):
    symbol = symbol_analysis["symbol"]
    max_out = symbol_analysis["max_out"]
    days = symbol_analysis["days"]
    if max_out != 0:
        hour = max_out["hour"]
        t = max_out["t"]
        income = max_out["income"]
        scale = max_out["scale"]
        price = max_out["price"]
        amount = symbol_analysis["amount"]
        vol = symbol_analysis["vol"]
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='password',
                                     db='hb',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `analysis_result` (`analysis_time`, `symbol`, `s_hour`, `t`, `income`, `scale`, `current`, `price`,`amount`,`vol`,`days`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (analysis_time, symbol, hour, t, income, scale, 1, price,amount,vol,days))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()


def initial_analysis_result():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='hb',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "update `analysis_result` set `current` = 0 "
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()


# 运行
if __name__ == '__main__':
    symbol_list = get_eth_symbol_list()

    dt = datetime.now()
    initial_analysis_result()
    print(dt)

    for symbol in symbol_list:
        try:
            symbol_analysis = get_symbol_analysis(symbol, 0.95)

            print(symbol_analysis["symbol"] + " max_out: ")
            print(symbol_analysis["max_out"])
            print(symbol_analysis["days"])

            submit_analysis_result(dt, symbol_analysis)
            print("-------------------------------------------")
        except Exception:
            pass
        else:
            pass

'''
get_symbol_analysis('veneth', 0.95, True)
'''
