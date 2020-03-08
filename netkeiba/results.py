import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime
from datetime import timedelta

#url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=202006020102&rf=shutuba_submenu"#shutubahyo page
url = "https://race.netkeiba.com/race/result.html?race_id=202006020102&rf=race_submenu"#results page


#着順、オッズをリストで返す
def getRaceResult(day):
    #url = "https://race.netkeiba.com/race/result.html?race_id="+day+"&rf=race_submenu"
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.content,'html.parser')
    name = soup.find_all("tr", class_="HorseList")

    results = []

    for na in name:
        #2重リスト用
        temp = []
        #馬名
        horse = na.find("span", class_="Horse_Name")
        temp.append(horse.text.strip())
        #オッズ
        odds = na.find("td", class_="Odds Txt_R")
        temp.append(odds.text.strip())
        #着順
        rank = na.find("div", class_="Rank")
        temp.append(rank.text.strip())
        #馬番（ソート用）
        umaban = na.find("td", class_="Num Txt_C")
        temp.append(int(umaban.text.strip()))
        results.append(temp)
    

    results.sort(key=lambda x: x[3])#2列めを基準にソート

    for i in results:
        i.pop(3)

    for i in results:
        print(i)
    return results

getRaceResult(2020)


#getResults("202006020103")

#file in out
# f = open('datasets/'+"urlの数字"+'.csv','w',newline="")
# f.write("aaa")
# f.close()