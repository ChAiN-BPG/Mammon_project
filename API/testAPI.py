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
