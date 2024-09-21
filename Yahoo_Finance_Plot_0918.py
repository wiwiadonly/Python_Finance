#!/usr/bin/env python
# coding: utf-8

# # yahoo_fin套件安裝

# In[3]:


get_ipython().getoutput('pip install yahoo_fin #')


# # 基本的DataFrame操作

# In[75]:


import pandas as pd

#基本的讀出資料
df=pd.read_csv("root"+"2330.TW"+".csv",index_col="Date",)
print("\n==========================================基本資料讀出==========================================")
print(df)

#用usecols 設定讀出欄位
df=pd.read_csv("root"+"2330.TW"+".csv",index_col="Date",usecols=["Date","Close"])
print("\n==========================================讀出Date和Close欄==========================================")
print(df)

#使用.head() 和.tail()來抓出最前五筆和最後五筆
print("\n==========================================讀出前五筆=========================================")
print(df.head())
print("\n==========================================讀出後五筆=========================================")
print(df.head())

#用.iloc[]設定起始行列和結尾行列
#使用方法df.iloc[起始行:結尾行 ,  起始列:結尾列]
print("\n==========================================讀出兩列=========================================")
print(df.iloc[0:2])


# # 進行股票資料抓取並存成csv

# In[5]:


import pandas as pd
from yahoo_fin.stock_info import get_data

#設定要抓取的股票代號
symbols=["2330.TW","2454.TW","2317.TW"]

for symbol in symbols:
    df = get_data(symbol)
    columns_dic={"open":"Open","high":"High","low":"Low","close":"Close","adjclose":"AdjClose","volume":"Volume"}
    df=df.rename(columns=columns_dic)#把小寫改成大寫
    df=df[["Open","High","Low","Close","AdjClose","Volume"]]#擷取需要得欄位(原有ticker去除掉)
    df.index.name="Date"#原index欄無名現在將其取名為date
    df.to_csv("root"+symbol+".csv")#將資料轉出成csv
    print(df.tail())


# # 建立當日收盤價與20天移動平均線的對比

# In[24]:


import pandas as pd
import matplotlib.pyplot as plt
symbols=["2330.TW","2454.TW","2317.TW"]

for symbol in symbols:
    #抓出Date和Close兩資料
    df=pd.read_csv("root"+symbol+".csv",index_col="Date",usecols=["Date","Close"])
    df=df.rename(columns={"Close":"Closing_Price"})
    df["MA_20"]=df["Closing_Price"].rolling(20).mean() #建立20天的Moving Average(移動平均線)
    df=df["2023":"2025"]#設定日期區間
    df.plot(title=symbol,figsize=(15,5),grid=True)
    plt.show()


# #  收盤價與30天內最高和30天內最低的比較

# In[79]:


import pandas as pd
import matplotlib.pyplot as plt
symbols=["2330.TW","2454.TW","2317.TW"]

for symbol in symbols:
    df=pd.read_csv("root"+symbol+".csv",index_col="Date",usecols=["Date","Close"])
    df=df.rename(columns={"Close":"Closing_Price"})
    df["Highest_30"]=df["Closing_Price"].rolling(30).max() #建立30天內的最高收盤價
    df["Lowest_30"]=df["Closing_Price"].rolling(30).min() #建立30天內的最低收盤價
    df=df["2023":"2025"]#設定日期區間
    df.plot(title=symbol,figsize=(15,5),grid=True)
    plt.show()


# # 整併股票資料並且繪圖

# In[65]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

#建立一個欲觀察的時間range
start=datetime.date(2023,1,1)#定義起始日期start
end=datetime.date.today()#以今天當作結束日期end
daterange=pd.date_range(start,end)#建立一個時間的range

#以建立好讀date_range作為index建立DataFrame
df_empty=pd.DataFrame(index=daterange)#建立一個空的DataFrame命名為df_empty
df_empty.index=pd.to_datetime(df_empty.index).strftime('%Y-%m-%d')#改變日期的表示方式 2023-01-01 00:00:00 -> 2023-01-01(這樣才有辦法對應到原資料裡的index欄)

#將不同股票依照日期對應上
symbols=["2330.TW","2454.TW","2317.TW"]
for symbol in symbols:
    df=pd.read_csv("root"+symbol+".csv",index_col="Date",usecols=["Date","Close"])
    df=df.rename(columns={"Close":symbol})#重新命名
    df_empty=df_empty.join(df).dropna()
print("==============對應上之後的每日收盤價表==============\n")
print(df_empty)
df_empty.plot(figsize=(15,5),grid=True)
print("\n\n\n==========================================對應上之後的每日收盤價圖==========================================")
plt.show()

#把第一天當作1進行常態化
df_Normal=df_empty/df_empty.iloc[0]
df_Normal.plot(figsize=(15,5),grid=True)
print("\n==========================================正規化後的每日收盤價比例圖==========================================")
plt.show()

#模擬投資組合中權重的概念進行圖表繪製
W=[0.3,0.4,0.3]#設定權重
df_Weighted=df_Normal*W#給權重後的投資組合累計報酬率
df_Weighted["WeightedPortfolio"]=df_Weighted.sum(axis=1)
df_Weighted[["WeightedPortfolio"]].plot(figsize=(15,5),grid=True)
print("\n==========================================設定權重之後的投資組合累積報酬率表==========================================")
plt.show()

#將每股的投資報酬率及組合累積報酬率呈現在圖表上
df_New=df_Normal.join(df_Weighted[["WeightedPortfolio"]])
df_New.plot(title="WeightedPortfolio vs Individual Stock Performance",figsize=(15,5),grid=True)
print("\n==========================================一起呈現之後的圖表==========================================")
plt.show()





