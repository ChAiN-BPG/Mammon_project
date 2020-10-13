## เปลี่ยน timeframe จาก 1M ไป 30M เกิดปัญหาที่ dataset ว่า มีช่วงเวลาหายไป 
## อาจจะเเก้โดย รวบเวลาให้ใหญ่ขึ้นอาจช่วยได้ 
import sys
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime


## ====================================== M1_to_M30 =========================================

# def M1_to_M30(soruse) :
#     print("-------------------------------------------------------------")
#     print("                   M1_to_M30 is activated                    ")
#     print("-------------------------------------------------------------")
#     xl = pd.read_excel(soruse,  header=None)
#     tr_xl = xl.to_numpy()
#     dataset = tr_xl.tolist()
#     if len(dataset) != 0 : print("recived the dataset!!!")
#     else:
#         sys.exit("the dataset is error!!!")
#     timer = int(dataset[0][0].strftime("%M"))
#     output = []
#     print("-------------------------------------------------------------")
#     print("                 start change M1 to M30                      ")
#     print("-------------------------------------------------------------")
#     lenofit = len(dataset)
#     print("All dataset : "+str(lenofit))
#     setturn = dataset[0]
#     setstate = 30 if timer <= 30 else 60
#     for count,data in enumerate (dataset):
#         if timer != data[0].strftime("%M"):
#             timer += 1
#             continue
         
#         ## annouse
#         percent = (count / lenofit) * 100
#         percent = round(percent,2)
#         aqurter = int((count / lenofit) * 25)
#         tick = "*" * aqurter
#         remain = "-" * (25 - aqurter)
#         print("["+tick+remain+"] " + "completed : "+ str(percent) + " %")
#     print("-------------------------------------------------------------")
#     print("write to excel")
#     df = pd.DataFrame(data=output)
#     df.to_excel('dataset/Rdataset_GU/GBPUSD-2000_30M.xlsx',header=None,index=None)
#     print("-------------------------------------------------------------")
#     print("                   end change M1 to M30                      ")
#     print("-------------------------------------------------------------")


## ====================================== M1_to_H1 =========================================


# def M1_to_H1(soruse) :
#     print("-------------------------------------------------------------")
#     print("                   M1 to H1 is activated                     ")
#     print("-------------------------------------------------------------")
#     xl = pd.read_excel(soruse,  header=None)
#     tr_xl = xl.to_numpy()
#     dataset = tr_xl.tolist()
#     if len(dataset) != 0 : print("recived the dataset!!!")
#     else:
#         sys.exit("the dataset is error!!!")
#     timer = int(dataset[0][0].strftime("%H"))
#     output = []
#     print("-------------------------------------------------------------")
#     print("                 start change M1 to H1                       ")
#     print("-------------------------------------------------------------")
#     lenofit = len(dataset)
#     print("All dataset : "+str(lenofit))
#     setturn = dataset[0]
#     for count,data in enumerate (dataset):
#         if timer != int(data[0].strftime("%H")):
#             output.append(setturn)
#             setturn = data
#             timer = int(data[0].strftime("%H"))
#         setturn[4] = data[4]
#         if data[2] > setturn[2] :
#             setturn[2] = data[2]
#         if data[3] < setturn[3]:
#             setturn[3] = data[3]
#         ## annouse
#         percent = (count / lenofit) * 100
#         percent = round(percent,2)
#         aqurter = int((count / lenofit) * 25)
#         tick = "*" * aqurter
#         remain = "-" * (25 - aqurter)
#         print("["+tick+remain+"] " + "completed : "+ str(percent) + " %")
#     print("-------------------------------------------------------------")
#     print("write to excel")
#     df = pd.DataFrame(data=output)
#     df.to_excel('dataset/Rdataset_GU/GBPUSD-2019_H1.xlsx',header=None,index=None)
#     print("-------------------------------------------------------------")
#     print("                   end change M1 to H1                       ")
#     print("-------------------------------------------------------------")


# ====================================== H1_to_H4 =========================================



def H1_to_H4(soruse) :
    print("-------------------------------------------------------------")
    print("                   H1 to H4 is activated                    ")
    print("-------------------------------------------------------------")
    xl = pd.read_excel('ML_TEST/Data/Timeframe_data/'+str(soruse)+'/GBPUSD-'+str(soruse)+'_H1.xlsx',  header=None)
    tr_xl = xl.to_numpy()
    dataset = tr_xl.tolist()
    if len(dataset) != 0 : print("recived the dataset!!!")
    else:
        sys.exit("the dataset is error!!!")
    timer = 0
    output = []
    print("-------------------------------------------------------------")
    print("                 start change H1 to H4                       ")
    print("-------------------------------------------------------------")
    lenofit = len(dataset)
    Isnext = False
    print("All dataset : "+str(lenofit))
    setturn = dataset[0]
    for count,data in enumerate (dataset):
        if Isnext: 
            setturn = data
            timer +=1
            Isnext = False
            continue
        setturn[4] = data[4]
        if data[2] > setturn[2] :
            setturn[2] = data[2]
        if data[3] < setturn[3]:
            setturn[3] = data[3]
        timer += 1
        if timer  == 4:
            output.append(setturn)
            Isnext = True
            timer = 0
        ## annouse
        percent = (count / lenofit) * 100
        percent = round(percent,2)
        aqurter = int((count / lenofit) * 25)
        tick = "*" * aqurter
        remain = "-" * (25 - aqurter)
        print("["+tick+remain+"] " + "completed : "+ str(percent) + " %")
    print("-------------------------------------------------------------")
    print("write to excel")
    df = pd.DataFrame(data=output)
    df.to_excel('ML_TEST/Data/Timeframe_data/'+str(soruse)+'/GBPUSD-'+str(soruse)+'_H4.xlsx',header=None,index=None)
    print("-------------------------------------------------------------")
    print("                   end change H1 to H4                       ")
    print("-------------------------------------------------------------")


# ====================================== M1_to_D1 =========================================


def H1_to_D1(year) :
    print("-------------------------------------------------------------")
    print("                   M1 to D1 is activated                    ")
    print("-------------------------------------------------------------")
    xl = pd.read_excel('ML_TEST/Data/Timeframe_data/'+str(year)+'/GBPUSD-'+str(year)+'_H1.xlsx',  header=None)
    tr_xl = xl.to_numpy()
    dataset = tr_xl.tolist()
    if len(dataset) != 0 : print("recived the dataset!!!")
    else:
        sys.exit("the dataset is error!!!")
    timer = int(dataset[0][0].strftime("%d"))
    output = []
    print("-------------------------------------------------------------")
    print("                 start change M1 to D1                       ")
    print("-------------------------------------------------------------")
    lenofit = len(dataset)
    Isnext = False
    print("All dataset : "+str(lenofit))
    setturn = dataset[0]
    for count,data in enumerate (dataset):
        if timer != int(data[0].strftime("%d")):
            output.append(setturn)
            Isnext = True
        if Isnext: 
            setturn = data
            timer = int(data[0].strftime("%d"))
            Isnext = False
            continue
        setturn[4] = data[4]
        if data[2] > setturn[2] :
            setturn[2] = data[2]
        if data[3] < setturn[3]:
            setturn[3] = data[3]
        ## annouse
        percent = (count / lenofit) * 100
        percent = round(percent,2)
        aqurter = int((count / lenofit) * 25)
        tick = "*" * aqurter
        remain = "-" * (25 - aqurter)
        print("["+tick+remain+"] " + "completed : "+ str(percent) + " %")
    print("-------------------------------------------------------------")
    print("write to excel")
    df = pd.DataFrame(data=output)
    df.to_excel('ML_TEST/Data/Timeframe_data/'+str(year)+'/GBPUSD-'+str(year)+'_D1.xlsx',header=None,index=None)
    print("-------------------------------------------------------------")
    print("                   end change M1 to D1                       ")
    print("-------------------------------------------------------------")


# ====================================== prepro =========================================


# def prepro (data):
#     outdata = []
#     isfrist = True
#     timer = 0
#     lastdata = []
#     for x in data:
#         if isfrist:
#             timer = x[0].strftime("%M")
#             isfrist = False ; timer = int(timer) + 1 ; lastdata = x
#             outdata.append(x)
#             continue
#         if int(x[0].strftime("%M")) == timer:
#             lastdata = x
#             outdata.append(x)
#             continue
#         while timer !=  int(x[0].strftime("%M")) :
#             timeNow = x[0].strftime("%Y-%m-%d, %H:")
#             timeNow += str(timer)
#             outdata.append([timeNow,(lastdata[1]+x[1])/2,(lastdata[2]+x[2])/2,(lastdata[3]+x[3])/2,(lastdata[4]+x[4])/2])
#             timer+= 1
#     return outdata

        
## ------------------------ code --------------------------------------------------

H1_to_D1(2002)

# for x in range(2003 , 2020):
#     H1_to_D1(x)

# data = "dataset/dataset_GBPUSA/DAT_XLSX_GBPUSD_M1_202005.xlsx"
# xl = pd.read_excel(data ,  header=None)
# tr = xl.to_numpy()
# dataset = tr.tolist()

# print(dataset[0][0].strftime("%M"))
# redata = tr_xl[:,1:]
# print(redata)
# arr_xl = tr_xl.tolist()

# numarr = prepro(arr_xl)
# df = pd.DataFrame(data=numarr)
# xl.to_csv('file_name.csv')




# print(arr_xl[0][0].strftime("%M"))
# print(tr_xl[0,0])
# print(xl[4])

# date = tr_xl[0,0]
# dt_object = datetime.fromtimestamp(date)
# time = date.strftime("%M")
# if int(time) < 30 : print(True)
# print("Min:", time)
# print(date)



## ploting graph 

# plt.figure(figsize=(10,10))
# plt.plot(xl[0], xl[4])
# plt.xlabel("date")
# plt.ylabel("$ price")
# plt.title("DIS Stock Price ")
# plt.show()


## ================ test ===============================

# data = [[-1, 2, 11], [-0.5, 6, 13], [6, 10, 16], [1, 18, 20]]
# arrdata = np.array(data)
# print(arrdata)
# scaler = MinMaxScaler()
# print(scaler.fit(arrdata))
# print(scaler.data_max_)
# print(scaler.transform(arrdata))
# print(scaler.transform([[2, 2, 2]]))

# print(scaler.inverse_transform([[1.2,1,-2]]))
# print("=======================================")



# test = [1,2,3,4,5,6,67,7,8,9,9,0,55,1,11,2,3,3,4,5,5,6,7,7]
# for count in range(3,len(test)+1):
#     print("train : "+str(test[count-3:count]))
