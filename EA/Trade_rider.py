import traderFX as TF

rez = TF.traderFX(balance=200)
rez.GetData(money="GBPUSD",start_year=2004,timeframe="H1")
# print(rez.dataset)
class smatrade():
    def __init__(self,index):
        self.ema12 = rez.EMA(index,12)
        self.ema36 = rez.SMA(index,26)
        self.adx14 = rez.ADX(index,7)
    def next (self,index,tick):
        if rez.Crossover(self.ema12,self.ema36):
            rez.last_cross = "SELL"
        if rez.Crossover(self.ema36,self.ema12):
            rez.last_cross = "BUY"
        if len(rez.order) >= 1:
            if self.adx14[1] < 40:
                rez.send_signal(tick,"close",order_id = 0)
        if len(rez.order) < 1:
            if rez.last_cross == "BUY":
                if rez.Touch(tick,self.ema12):
                    rez.send_signal(tick,"BUY")
                    rez.last_cross = None
            if rez.last_cross == "SELL":
                if rez.Touch(tick,self.ema12):
                    rez.send_signal(tick,"SELL")
                    rez.last_cross = None

rez.run(smatrade)