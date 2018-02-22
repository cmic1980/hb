import time
from task import *
from api.HuobiServices import *

kline = get_kline('eoseth', '60min', 2000)

order_list = load_pending_order_list()
print(order_list)

s = datetime.datetime(2018, 2, 22, 13)
t = time.mktime(s.timetuple())
print(t)