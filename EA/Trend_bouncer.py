import traderFX as TF

test = TF.traderFX(balance=200000,lot= "standard",path_save = "data/trade_data/Trend_bouncer/action_Trend_bouncer_2019.csv")
test.get_data(start_year = 2019)
test.pre_nignal = None
# # print(test.balance)
# # print(test.budget)
# # print(test.spread)
# # print(test.lot)
# # print(test.leverage)
class test_strategy:
    def __init__(self,dataset):
        list_indicator = test.set_indicator([["BB",12,2],["BB",12,4]])
        self.BB2 = list_indicator[0]
        self.BB4 = list_indicator[1]
    def next (self,index,tick):
        if test.Crossprice(index,self.BB2[1]):
            test.pre_nignal = "BUY"
        if test.Crossprice(index,self.BB2[2]):
            test.pre_nignal = "SELL"
        if len(test.order) >= 1:
            test.Take_profit(index,tick,0)
        if len(test.order) >= 1:
            test.stop_loss(index,tick,0)
        if len(test.order) < 1:
            if test.Crossprice(index,self.BB2[0]):
                if test.pre_nignal == "BUY":
                    SL = self.BB4[2][index]
                    TP = ((tick[4] - SL)*1) + tick[4]
                    test.send_order(index,tick,"BUY",TP=TP,SL=SL)
                    test.pre_nignal = None
                if test.pre_nignal == "SELL":
                    SL = self.BB4[1][index]
                    TP =tick[4] - ((SL-tick[4])*1)  
                    test.send_order(index,tick,"SELL",TP=TP,SL=SL)
                    test.pre_nignal = None

test.run(test_strategy)
