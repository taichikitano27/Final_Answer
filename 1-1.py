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
    pattern =re.compile(r'(?P<pref>.{2,3}[都道府県])(?P<city>.+?[市区町村])(?P<addr>\D+[\d\-]*)(\s*)(?P<bldg>.*)')
    match = re.match(pattern,address)
    if match:
        return match.group('pref'),match.group('city'),match.group('addr'),match.group('bldg')
    else:
        return '','','',''
def get_store_info(url):
    response= request.urlopen(url)
    soup=BeautifulSoup(response)
    response.close()
    soups=soup.find('table',class_='basic-table')
    all_store=[]
    store_info={}
    for row in soup.find_all('tr'):
        th=row.find('th')
        td=row.find('td')
        if th and td:
            label=th.get_text()
            value=td.get_text()
            store_info[label]=value
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
    cleaned['URL']=''
    cleaned['SSL']=''
    return cleaned

def main():
    store_urls=[
    'https://r.gnavi.co.jp/6geetz310000/',
    'https://r.gnavi.co.jp/k781330/',
    'https://r.gnavi.co.jp/c788200/?sc_type=eki&sc_area=0005522&sc_dsp=rs_344134',
    'https://r.gnavi.co.jp/hhdhhsz30000/',
    'https://r.gnavi.co.jp/8znn52xm0000/',
    'https://r.gnavi.co.jp/shuvfe5v0000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_350551',
    'https://r.gnavi.co.jp/m5xj8rju0000/',
    'https://r.gnavi.co.jp/5v5k4ubn0000/',
    'https://r.gnavi.co.jp/7x40ugd00000/',
    'https://r.gnavi.co.jp/rx6cce2t0000/',
    'https://r.gnavi.co.jp/pem91ubm0000/',
    'https://r.gnavi.co.jp/k311725/',
    'https://r.gnavi.co.jp/c7rkgku00000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349457',
    'https://r.gnavi.co.jp/6yw9n9fx0000/',
    'https://r.gnavi.co.jp/npss91zh0000/',
    'https://r.gnavi.co.jp/8n0k2ykk0000/',
    'https://r.gnavi.co.jp/c081100/',
    'https://r.gnavi.co.jp/4av2aa0m0000/',
    'https://r.gnavi.co.jp/hmajj5e30000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349909',
    'https://r.gnavi.co.jp/7y9ua96b0000/',
    'https://r.gnavi.co.jp/k844407/',
    'https://r.gnavi.co.jp/6geetz310000/',
    'https://r.gnavi.co.jp/6rpbr5nm0000/',
    'https://r.gnavi.co.jp/fxy8wt950000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349749',
    'https://r.gnavi.co.jp/k305900/',
    'https://r.gnavi.co.jp/gjh12k730000/',
    'https://r.gnavi.co.jp/j1gxrg120000/',
    'https://r.gnavi.co.jp/gxe6zfw30000/',
    'https://r.gnavi.co.jp/kabm500/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349815',
    'https://r.gnavi.co.jp/98655vc60000/',
    'https://r.gnavi.co.jp/r0u09ajz0000/',
    'https://r.gnavi.co.jp/k207326/',
    'https://r.gnavi.co.jp/k844408/',
    'https://r.gnavi.co.jp/kbby400/',
    'https://r.gnavi.co.jp/k724700/',
    'https://r.gnavi.co.jp/pt01pmz70000/',
    'https://r.gnavi.co.jp/b98tgc260000/',
    'https://r.gnavi.co.jp/gxe6zfw30000/',
    'https://r.gnavi.co.jp/k002703/',
    'https://r.gnavi.co.jp/8v5cz9xe0000/',
    'https://r.gnavi.co.jp/7x40ugd00000/',
    'https://r.gnavi.co.jp/57a7a6ap0000/',
    'https://r.gnavi.co.jp/hmajj5e30000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349909',
    'https://r.gnavi.co.jp/k763304/',
    'https://r.gnavi.co.jp/bdh1e2fy0000/',
    'https://r.gnavi.co.jp/genj7wdb0000/',
    'https://r.gnavi.co.jp/k0px0bfj0000/',
    'https://r.gnavi.co.jp/dp56pcwr0000/?sc_type=eki&sc_area=0005522&sc_dsp=rs_349973',
    'https://r.gnavi.co.jp/npss91zh0000/',
    'https://r.gnavi.co.jp/8n0k2ykk0000/'
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
    df.to_csv('test1-1.csv', index=False, encoding='utf-8',quoting=1)

main()  






