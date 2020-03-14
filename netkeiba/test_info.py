import sys
import requests
import re
from bs4 import BeautifulSoup
import warnings
import csv
import pprint
import time
import datetime
from keiba_function import getRaceNum, getSexNum, getShibadaNum, getStateNum, getRaceResult, TtoF
from datetime import timedelta

def info(date):
	
	url = "https://race.netkeiba.com/race/shutuba_past.html?race_id="+date+"&rf=shutuba_submenu"
	html = requests.get(url)
	html.encoding =html.apparent_encoding
	soup = BeautifulSoup(html.content,'lxml',from_encoding="euc-jp")

	#racedata01に欲しい物が全部入っています
	baseinfo = soup.find("div",class_ = "RaceData01")
	#appendする用のリストになります
	header = []
	#spanタグに全部あります　全部で3要素です
	data = baseinfo.find_all("span")
	#1つ目の要素に芝ダートと距離が入っているのでそれを分けた上で数値化します
	shiba,kyori = data[0].text.strip()[:1],data[0].text[2:6]
	#芝ダと距離をappendします
	header.append(getShibadaNum(shiba))
	header.append(kyori)
	#馬場状態を数値化したものをappendします
	header.append(getStateNum(data[2].text[-1:]))
	
info("202009010510")
