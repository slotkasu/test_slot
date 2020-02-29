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

url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=202006020102&rf=shutuba_submenu"


html = requests.get(url)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.content,'html.parser')
name = soup.find_all("td")

ls = []
for na in name:
    temp = na.get_text()
    temp = re.sub("\n{1,}"," ",temp)
    temp = temp.replace("\xa0","")
    temp = temp.replace(" ","",1)
    
    if "[馬記号]" in temp:
        print("\n\n")
        break
    elif "--◎◯▲" in temp:
        continue
    if na.get_text().strip() != "":
        ls.append(temp)
        #print(temp)

#for i in ls:#ノーブレークスペース(\xa0)がところどころ入ってる
    #print(re.split(" |\xa0|  ",i))

for i in ls:
    print(i)
"""
,,ジャングルポケット,, グランクロワ,,カラフルトーク,(サンデーサイレンス),美浦・大和田  ,中16週,,456kg(+6),,---.-,**,,,,
ジャングルポケット キョウエイリヴァルキョウエイダルク (ネオユニヴァース) 美浦・武藤   中4週466kg(-2)---.- **

,,,2019.06.02 東京,4,,,2歳新馬,,,,,,,,,,,,,,,,,,芝1600 1:37.4 良,7頭 3番 7人 大塚海渡 51.0,3-3 (34.6) 392(0),モーベット(0.5),,,,,
 2019.06.01 東京 11 2歳新馬芝1400 1:25.4 良 12頭 10番 6人 藤田菜七 51.0 1-1 (35.8) 428(0) カイトレッド(1.5)
"""