from datetime import datetime
import MetaTrader5 as mt5
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def check():
    
    
    pass 

def send_order():
   pass

def close_order():
    pass

def get_observation():
    pass


mt5.initialize()
selected = mt5.symbol_select("GBPUSD",True)
if not selected:
    print("Failed to select GBPUSD, error code =",mt5.last_error())
else:
    symbol_info=mt5.symbol_info("GBPUSD")
    print(symbol_info)
    print("GBPUSD: currency_base =",symbol_info.currency_base,"  currency_profit =",symbol_info.currency_profit,"  currency_margin =",symbol_info.currency_margin)
    print()
account_data = mt5.account_info()
print("Mammon expert advisor activated !!")
print("welcome " + str(account_data.name))
print("Your balance is " + str(account_data.balance))
mt5.shutdown()

############## test #################

