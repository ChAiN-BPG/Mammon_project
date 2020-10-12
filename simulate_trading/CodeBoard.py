import core
import pandas as pd
import talib as ta 
import numpy as np

res = core.Simforex()

print(res.lot)
# print(res.budget)
print(res.leverage)
res.set_Leverage("1:100")
print(res.leverage)
res.set_lot("micro")
res.add_budget(100)
res.change_risk(0.1)
res.add_period("GBPUSD",2004,"H1")
# Test_data = pd.DataFrame(res.data)
# print(Test_data)
res.add_indicator(active = [1,1,0,0,0,0,0])
res.run_sim(-1)



