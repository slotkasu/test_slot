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
#from results import getResults

year="2019"

#target url
url = "https://race.netkeiba.com/race/shutuba_past.html?race_id=201906020111&rf=shutuba_submenu"

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
		#print("\n\n")
		break
	elif na.get_text().strip() != "":
		ls.append(temp)
		
ls_new = [[]]
count = 0
flag = 0#馬番、枠番、馬情報を1行に結合するためのフラグです
evac = []
dirt = []

for i in ls:#リストを2重リストにしています
	if ("芝1000" in i) and ("新潟" in i):
		i.pop(3)
	if len(i) == 15:
		i.insert(12,"0")
	elif len(i) == 17:
		i.pop(3)

	ls_new.append(i)#すべての要素を入れます

	if len(i) == 1:#長さが1（馬番のみ、枠番のみ、よくわからん予想印）だとここで弾かれます
		if count == 2:
			del ls_new[-1]
			count = 0
			flag = 1#長さ1の要素が3つ続くとフラグがオンになります
			continue
		elif count == 0:
			temp = [ls_new.pop(-1)]#予想印の要素を飛ばします
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
	print(i)


# for i in ls_new:
#	 print(i)

# for i in ls_new:
#	 if len(i) > 15:
#		 for j in i:
#			 if re.match(r"ダ\d*|芝\d",j) != None:# or "ダ2" or "芝2" or "芝3"
#				 print(j)

#1行目のごみを削除

ls_new.pop(0)

sex=["牡","牝","セ"]

new_list=[]
temp_list=[0,0]
uma_ban=1
for i in ls_new:
	
	#今だけの処理
	# if uma_ban==3:
	# 	break
	
	if i[1] == str(uma_ban):
		print(i)
		if len(temp_list) != 0:
			uma_ban+=1
			#print(uma_ban)
			#temp_listが空では無ければ書き込み。
			new_list.append(temp_list)
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

		
		#print(temp_list)

	elif "20" in i[0]:
		print(i)
		#競馬場
		temp_list.append(i[1])
		#人気
		temp_list.append(i[2])
		#芝ダ
		temp_list.append(i[4][0])
		#距離
		temp_list.append(re.search(r'\d+',i[4]).group())
		#タイム
		temp_list.append(i[5])
		#馬場状態
		temp_list.append(i[6])
		#頭数
		print(i[7])
		temp_list.append(re.search(r'\d+',i[7]).group())
		#馬番
		temp_list.append(re.search(r'\d+',i[8]).group())
		#人気
		print(i[9])
		temp_list.append(re.search(r'\d+',i[9]).group())
		#斤量
		temp_list.append(i[11])
		#通過順
		#空のリストの数
		through=i[12].split('-')
		empty=4-len(through)
		for j in through:
			temp_list.append(j)
		for j in range(empty):
			temp_list.append(0)
		#３ハロン
		temp_list.append(re.findall(r'\((.*)\)',i[13])[0])
		#体重
		temp_list.append(re.search(r'\d+',i[14]).group())
		#体重増減
		temp_list.append(re.findall(r'\((.*)\)',i[14])[0])
		#着差
		temp_list.append(re.findall(r'\((.*)\)',i[15])[0])


new_list.append(temp_list)

writer.writerows(new_list)
print("お疲れさまでした（朧）")
