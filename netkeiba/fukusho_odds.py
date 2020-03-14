import sys
import requests
import re
from bs4 import BeautifulSoup
import csv
import pprint
import time
import datetime
from keiba_function import getRaceNum, getSexNum, getShibadaNum, getStateNum, getRaceResult, TtoF
from datetime import timedelta

days = "202007010505"

url = "https://race.netkeiba.com/odds/index.html?type=b1&race_id="+days+"&rf=shutuba_submenu"
html = requests.get(url)
html.encoding =html.apparent_encoding
soup = BeautifulSoup(html.content,'lxml',from_encoding="euc-jp")
tags = soup.find("div",id="odds_fuku_block")

print(tags)

