import traderFX as TF

test = TF.traderFX(balance=200,lot= "mini")
test.get_data(currancy="GBPUSD",start_year=2006)
test.last_cross = None
# # print(test.balance)
# # print(test.budget)
# # print(test.spread)
# # print(test.lot)
# # print(test.leverage)
class Trade_rider:
    def __init__(self,dataset):
        # self.sma12 = ta.SMA(dataset.loc[:,"close"],12)
        # self.sma36 = ta.SMA(dataset.loc[:,"close"],36)
        list_indicator = test.set_indicator([["EMA",12],["EMA",36],["ADX",7]])
        self.ema12 = list_indicator[0]
        self.ema36 = list_indicator[1]
        self.adx14 = list_indicator[2]
    def next (self,index,tick):
        if test.Crossover(index,self.ema12,self.ema36):
            test.last_cross = "SELL"
        if test.Crossover(index,self.ema36,self.ema12):
            test.last_cross = "BUY"
        if len(test.order) >= 1:
            if self.adx14[index] < 40:
                test.send_order(index,tick,"close",order_id=0)
            else : test.stop_loss(index,tick,0)
        if len(test.order) < 1 :
            if test.last_cross == "SELL" and test.Crossprice(index,self.ema12) and self.adx14[index] > 40:
                SL = self.ema36[index] if self.ema36[index] > tick[4] + 0.0003 else tick[4] + 0.0003
                test.send_order(index,tick,"SELL",SL=SL)
                test.last_cross = None
            if test.last_cross == "BUY" and test.Crossprice(index,self.ema12) and self.adx14[index] > 40:
                SL = self.ema36[index] if self.ema36[index] < tick[4] + 0.0003 else tick[4] + 0.0003
                test.send_order(index,tick,"BUY",SL=SL)
                test.last_cross = None

test.run(Trade_rider)
# # print(test.dataset)
# # print(test.ready)
