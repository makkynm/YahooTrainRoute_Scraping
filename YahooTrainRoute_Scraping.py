#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#必要なライブラリをインポート
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


# In[ ]:


#input fileの読み込み tab区切り
InputFilePath = "StationCombination.csv"
df_base = pd.read_table(InputFilePath)
SearchURLs = df_base["SearchURL"].values.tolist()
Origins = df_base["Origin"].values.tolist()
Destinations = df_base["Destination"].values.tolist()


# In[ ]:


Results = []
HeaderNames = ["SearchURL", "Origin", "Destination", "Time", "Fare", "Transfer", "Priority","Comment"]

for iURL, url in enumerate(SearchURLs):
    print(str(iURL+1) + " / " + str(len(SearchURLs)))
    try:
        #データ取得
        result = requests.get(url)
        c = result.content
        #HTMLを元に、オブジェクトを作る
        soup = BeautifulSoup(c, "html.parser")
        #ページ数を取得
        body = soup.find("body")
        RouteListElem = body.find("ul",{'class':'routeList'})
        
        if RouteListElem == None:
            ErrorElem = body.find("div",{'class':'boxError'})
            ErrorMessage = ErrorElem.get_text()
            Detail = [SearchURLs[iURL], Origins[iURL], Destinations[iURL], "", "", "", "", ErrorMessage]
            Results.append(Detail) 
            time.sleep(5)
        else:
            WarningElem = body.find("dl",{'class':'boxResearch'})
            if WarningElem == None:
                Comment = ""
            else:
                Comment = WarningElem.get_text()
            
            TimeElem = RouteListElem.find_all("li",{'class':'time'})
            Times = [elem.find("span",{'class':'small'}).get_text() for elem in TimeElem]
            Time = ' --- '.join(Times)

            FareElem = RouteListElem.find_all("li",{'class':'fare'})
            Fares = [elem.get_text() for elem in FareElem]
            Fare = ' --- '.join(Fares)

            TransferElem = RouteListElem.find_all("li",{'class':'transfer'})
            Transfers = [elem.get_text() for elem in TransferElem]
            Transfer = ' --- '.join(Transfers)    

            PriorityElem = RouteListElem.find_all("li",{'class':'priority'})
            Priorities = [elem.get_text() for elem in PriorityElem]
            Priority = ' --- '.join(Priorities)  

            Detail = [SearchURLs[iURL], Origins[iURL], Destinations[iURL], Time, Fare, Transfer, Priority,Comment]
            Results.append(Detail)
            time.sleep(5)
    except requests.exceptions.RequestException as e:
        print("エラー : ",e)
        time.sleep(5)

df = pd.DataFrame(Results, columns = HeaderNames)
filename = "Yahoo_Route.csv"
df.to_csv(filename)
