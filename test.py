import time
import math
from task import *
from api.HuobiServices import *


s = datetime.datetime(2018, 2, 24,21)
t = time.mktime(s.timetuple())
print(t)

symbol_list = get_eth_symbol_list()
print(symbol_list)
