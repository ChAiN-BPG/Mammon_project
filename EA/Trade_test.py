import traderFX as TF

rez = TF.traderFX(balance=200000,lot= "standard",path_save = "data/trade_data/Trade_rider/action_Simple_ema_2019.csv")
rez.get_data(start_year = 2019)
class test_trade():
    def __init__(self,index):
        list_indicator = rez.set_indicator([["EMA",12],["EMA",36]])
        self.ema12 = list_indicator[0]
        self.ema36 = list_indicator[1]
    
    def next (self,index,tick):
        if len(rez.order) >= 1:
            if rez.Crossover(index,self.ema12,self.ema36):
                rez.send_order(index,tick,"close",order_id = 0)
            if rez.Crossover(index,self.ema36,self.ema12):
                rez.send_order(index,tick,"close",order_id = 0)
        if len(rez.order) < 1 :
            if rez.Crossover(index,self.ema12,self.ema36):
                rez.send_order(index,tick,"SELL")
            if rez.Crossover(index,self.ema36,self.ema12):
                rez.send_order(index,tick,"BUY")

rez.run(test_trade)