import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime
from keiba_function import getRaceNum, getSexNum, getShibadaNum, getStateNum, getRaceResult, TtoF, getFuku
from datetime import timedelta
import sqlite3
from contextlib import closing
import glob

# データベース名
dbname = sqlite3.connect("keibadata.sqlite3")
c = dbname.cursor()

sql = 'insert into racenametable (race_number, racename) values (?,?)'

# レース番号とレース名を対応付けするための関数
# DBが完成したときに、SQL処理を付け足す
# 

def makeRaceName(date):
	url = "https://race.netkeiba.com/race/shutuba_past.html?race_id="+date+"&rf=shutuba_submenu"

	html = requests.get(url)
	html.encoding =html.apparent_encoding
	soup = BeautifulSoup(html.content,'lxml',from_encoding="euc-jp")
	
	#trタグのHorseListクラスからtr_[0-9]{2}のものだけを抽出
	horseLists = soup.find_all("tr",class_="HorseList",id=re.compile(r"tr_[0-9]+"))
	if len(horseLists) == 0:
		print("サイトが存在しないためスキップします。")
		return 3
	if soup.find("tr",class_="HorseList Cancel"):
		print("除外馬が存在するためスキップします。")
		return 1
	try:
		title = soup.find("div",class_="RaceName").text.strip()
	except:
		print("CANT GET RACE NAME")
		title = None

	user = (int(date),title)
	
	try:
		c.execute(sql,user)
		dbname.commit()
	except:
		print(date, title, "ERROR : already exists.")

	return 0

makeRaceName("201804030612")