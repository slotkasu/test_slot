# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)
options.add_argument("--log-level=3")

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# ブラウザでアクセスする
date="201808030411"

driver.get("https://race.netkeiba.com/odds/index.html?type=b1&race_id="+date+"&rf=shutuba_submenu")
# time.sleep(0.5)
# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# idがheikinの要素を表示
odds=soup.find("div", id="odds_fuku_block")
odds=odds.find_all("tr")
for i in odds:
	if not i == None:
		# name=i.find("td",class_="Horse_Name")
		# print(name)
		odd=i.find("td",class_="Odds Popular")
		if not odd == None:
			min_odds=odd.string.split()[0]
			max_odds=odd.string.split()[2]
			print(min_odds,max_odds)