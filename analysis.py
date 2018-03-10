
from api.HuobiServices import *

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
    for item in list:
        if item['open'] != 0:
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
    out["scale"] = c1 / (c1 + c2)

    return out

def get_symbol_analysis(symbol, probability, show_detail=False):
    kline_list = get_kline_ex(symbol,"60min",2000)
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

    print(symbol + " max_out: ")
    print(max_out)
    print(len(kline_list))



symbol_list = get_eth_symbol_list()
for symbol in symbol_list:
    try:
        get_symbol_analysis(symbol, 0.95)
        print("-------------------------------------------")
    except Exception:
      pass
    else:
        pass

'''
get_symbol_analysis('payeth', 0.9, True)
'''
