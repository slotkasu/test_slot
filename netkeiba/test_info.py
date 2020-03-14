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
	baseinfo = soup.find("div",class_ = "RaceData01")
	for i in baseinfo:
		


info("202009010510")