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
from results import getResults

#target url
url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=202006020102&rf=shutuba_submenu"

def getCalendar(i):
	now = datetime.date.today()-datetime.timedelta(days = -i)
	string_date = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)
	return string_date


#file
f = open('keiba/'+getCalendar(0)+'out.csv','w',newline = "")
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

# for i in ls_new:
#     if len(i) > 15:
#         for j in i:
#             if re.match(r"ダ\d*|芝\d",j) != None:# or "ダ2" or "芝2" or "芝3"
#                 print(j)

#1行目のごみを削除
ls_new.pop(0)

sex=["牡","牝","セ"]

uma_ban=1
for i in ls_new:
	#print(i)
	if i[1] == str(uma_ban):
		temp_list=[]
		temp_list.append(i[0])
		temp_list.append(i[1])
		#中〇週の数字部分を抽出
		temp_list.append(re.search(r'\d+',i[7]).group())
		#体重
		temp_list.append(re.search(r'\d+',i[8]).group())
		#体重増減
		temp_list.append(re.findall(r'\((.*)\)',i[8])[0])
		#性別
		temp_list.append(i[11][0])
		#馬齢
		temp_list.append(re.search(r'\d+',i[11]).group())
		#斤量
		temp_list.append(i[13])

		uma_ban+=1
		print(temp_list)

writer.writerows(ls_new)
print("お疲れさまでした（朧）")