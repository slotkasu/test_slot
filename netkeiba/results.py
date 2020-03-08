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
def getResults(day):
    url = "https://race.netkeiba.com/race/result.html?race_id="+day+"&rf=race_submenu"
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.content,'html.parser')
    name = soup.find_all("tr")

#span Horse_Name

    results = []
    temp = []
    count = 1
    for na in name:
        if re.search(r".人気",na.get_text()):
            break
        if (count == 1) or (count == 3) or (count == 11):#1：着順　3：馬番　11：オッズ
            temp.append(float(na.get_text().strip()))#flost
        if count == 15:#1行15要素
            results.append(temp)
            temp = []
            count = 0
        count += 1
    results.sort(key=lambda x: x[1])#2列めを基準にソート
    ###
    print("着順、馬番、オッズ")
    for i in results:
        print(i)
    ###
    return results




#getResults("202006020103")

#file in out
# f = open('datasets/'+"urlの数字"+'.csv','w',newline="")
# f.write("aaa")
# f.close()