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

#target url
#url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=202006020102&rf=shutuba_submenu"
url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=202009010111"

#file
f = open('keiba/out.csv','w',newline = "")
writer = csv.writer(f)

#beautifulsoup
html = requests.get(url)
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.content,'html.parser')
name = soup.find_all("td")

ls = []
for na in name:
    temp = na.get_text()
    temp = re.sub("\n{1,}"," ",temp)
    temp = temp.replace("\xa0"," ")
    temp = temp.replace(" ","",1)
    temp = temp.strip()
    temp = temp.split(" ")
    
    if "[馬記号]" in temp:
        print("\n\n")
        break
    elif na.get_text().strip() != "":
        ls.append(temp)
        
ls_new = [[]]
count = 0
flag = 0
evac = []

dirt = []
for i in ls:
    ls_new.append(i)

    if len(i) == 1:
        if count == 2:
            del ls_new[-1]
            count = 0
            flag = 1
            continue
        elif count == 0:
            temp = [ls_new.pop(-1)]
            count += 1
        else:
            temp.append(ls_new.pop(-1))
            count += 1
    elif flag == 1:
        if len(temp) == 2:
            temp.append(ls_new.pop(-1))
        else:
            temp.append(ls_new.pop(-1))
            
            for j in temp:
                for t in j:
                    if t == "":
                        continue
                    else:
                        
                        if re.search(r"芝\d\d00",t) != None:
                            dirt.append(t)
                        evac.append(t)
            ls_new.append(evac)
            evac = []
            flag = 0

for i in ls_new:
    if len(i) > 15:
        for j in i:
            if re.match(r"ダ\d*|芝\d",j) != None:# or "ダ2" or "芝2" or "芝3"
                print(j)



writer.writerows(ls_new)
print("お疲れさまでした（朧）")