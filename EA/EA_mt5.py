import MetaTrader5 as mt5 
import pandas as pd 
import numpy as np 

if not mt5.initialize(login=36223638, server="MetaQuotes-Demo",password="kctc2rca"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on connection status, server name and trading account
# print(mt5.terminal_info())
# # display data on MetaTrader 5 version
# print(mt5.version())
account_info=mt5.account_info()
account_info_dict = mt5.account_info()._asdict()
for prop in account_info_dict:
    print("  {}={}".format(prop, account_info_dict[prop]))
print()
# shut down connection to the MetaTrader 5 terminal
# mt5.shutdown()