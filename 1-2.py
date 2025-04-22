from urllib import request
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re 
import csv
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
def split_address(address):
    #正規表現で住所を分割
    pattern =re.compile(r'(?P<pref>.{2,3}[都道府県])(?P<city>.+?[市区町村])(?P<addr>\D+[\d\-]+)(\s*)(?P<bldg>.*)')
    match = re.match(pattern,address)
    if match:
        return match.group('pref'),match.group('city'),match.group('addr'),match.group('bldg')
    else:
        return '','','',''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
service = Service(executable_path=r"C:\\Program Files\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
def get_store_info(url):
    driver.get(url)
    time.sleep(3)
    table=driver.find_element(By.CLASS_NAME,"basic-table")
    rows=table.find_elements(By.TAG_NAME,"tr")
    store_info={}
    for row in rows:
        try:
            th = row.find_element(By.TAG_NAME, "th")
            td = row.find_element(By.TAG_NAME, "td")
            label = th.text.strip()
            value = td.text.strip()
            store_info[label] = value
        except:
            continue
    cleaned={}
    cleaned['店舗名']=re.sub(r'[ァ-ヴー]+$', '', store_info.get("店名", "").strip())
    tel_match = re.search(r'\d{2,4}-\d{2,4}-\d{4}', store_info.get("電話番号", ""))
    cleaned["電話番号"] = tel_match.group() if tel_match else ""
    address = store_info.get("住所", "")
    address = re.sub(r'〒\d{3}-\d{4}', '', address)
    address = re.sub(r"(大きな地図で見る|地図印刷)", "", address)
    address = address.replace('\r', '').replace('\n', ' ')          # 改行 → 半角スペース
    address = address.replace('　', ' ')                             # 全角スペース → 半角スペース
    address = re.sub(r'\s+', ' ', address) 
    address = address.strip()
    cleaned['メールアドレス']=''
    pref,city,addr,bldg=split_address(address)
    cleaned['都道府県']=pref
    cleaned['市区町村']=city
    cleaned['番地']=addr
    cleaned['建物名']=bldg
    try:
        a_tag=driver.find_elements(By.LINK_TEXT,"お店のホームページ")
        link=a_tag.get_attribute("href")
    except:
        link=''
    cleaned['URL']=link
    cleaned['SSL']=''
    return cleaned

def main():
    store_urls=[
    'https://r.gnavi.co.jp/shuvfe5v0000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_350551',
    'https://r.gnavi.co.jp/6geetz310000/',
    
    ]
    headers=['店舗名','電話番号','メールアドレス','都道府県','市区町村','番地','建物名','URL','SSL']
    data = []
    for url in store_urls:
        print(f"処理中: {url}")
        cleaned = get_store_info(url)
        tmp=[str(cleaned.get(col,'')).replace('\n','').replace(',','、')for col in headers]
        data.append(tmp)   
    print(data)
    df=pd.DataFrame(data,columns=headers)
    print(df)
    df.to_csv('test1-2.csv', index=False, encoding='utf-8',quoting=1)

main()  

