import traderFX as TF

rez = TF.traderFX(balance=500,lot = "micro")
rez.GetData(money="GBPUSD",start_year=2004,timeframe="H1")
class test_trade():
    def __init__(self,index):
        self.ema12 = rez.SMA(index,12)
        self.ema36 = rez.SMA(index,26)
    
    def next (self,index,tick):
        if len(rez.order) >= 1:
            if rez.Crossover(self.ema12,self.ema36):
                rez.send_signal(index,tick,"close",order_id = 0)
            if rez.Crossover(self.ema36,self.ema12):
                rez.send_signal(index,tick,"close",order_id = 0)
        if len(rez.order) < 1 :
            if rez.Crossover(self.ema12,self.ema36):
                rez.send_signal(index,tick,"SELL")
            if rez.Crossover(self.ema36,self.ema12):
                rez.send_signal(index,tick,"BUY")

rez.run(test_trade)