import MetaTrader5 as mt5

# if not mt5.initialize(login=14078, server="ThinkMarkets-Live",password="Sl8838450"):
if not mt5.initialize(login=38111485, server="MetaQuotes-Demo",password="test1234"): 
    print("initialize() failed, error code =",mt5.last_error())
    quit()
# mt5.initialize()
print(mt5.terminal_info())
print(mt5.version())
print(mt5.account_info())
print("wait you litle shit")
print(mt5.symbols_total())
print(mt5.symbol_info("GBPUSD"))
# selected=mt5.symbol_select("GBPUSD",True)
# if not selected:
#     print("Failed to select GBPUSD")
#     mt5.shutdown()
#     quit()
# lasttick=mt5.symbol_info_tick("GBPUSD")
# print(lasttick)
# # display tick field values in the form of a list
# print("Show symbol_info_tick(\"GBPUSD\")._asdict():")
# symbol_info_tick_dict = mt5.symbol_info_tick("GBPUSD")._asdict()
# for prop in symbol_info_tick_dict:
#     print("  {}={}".format(prop, symbol_info_tick_dict[prop]))


## send order 



## show all order 
orders=mt5.orders_total()
if orders>0:
    print("Total orders=",orders)
else:
    print("Orders not found")