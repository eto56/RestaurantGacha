import requests, json
import pandas as pd
from dotenv import load_dotenv
import os


env_path = "../.env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.environ["HOTPEPPER_API_KEY"]

BASE = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

def parse_shop_info(shop):
    """
    shop: Hot Pepper APIから得た1件分の辞書データ
    戻り値: 必要な情報を抜き出した辞書
    """
    def extract_name(field):
        v = shop.get(field)
        # v が辞書なら name を、そうでなければそのまま返す
        if isinstance(v, dict):
            return v.get('name')
        return v

    # budget は平均価格も入っていることがあるのでちょっと特別処理
    def extract_budget(field):
        v = shop.get(field)
        if isinstance(v, dict):
            return v.get('name'), v.get('average')
        # 文字列だけなら平均価格は None
        return v, None

    budget_name, average_price = extract_budget('budget')

    return {
        'id': shop.get('id'),
        'name': shop.get('name'),
        'name_kana': shop.get('name_kana'),
        'address': shop.get('address'),
        'station': shop.get('station_name') or shop.get('station'),
        'genre': extract_name('genre'),
        'sub_genre': extract_name('sub_genre'),
        'budget': budget_name,
        'average_price': average_price or shop.get('average_price'),
        'catch': shop.get('catch'),
        'lat': shop.get('lat'),
        'lng': shop.get('lng'),
        'url': (shop.get('urls') if isinstance(shop.get('urls'), str)
                else shop.get('urls', {}).get('pc')),
        'open_hours': shop.get('open') or shop.get('open_hours'),
        'close_day': shop.get('close') or shop.get('close_day'),
    }

 
# 1) 総数取得
r = requests.get(BASE, params={
    'key': API_KEY,
    'large_area': 'Z011',
    'format': 'json',
    'count': 1
})
N = r.json()['results']['results_available']

print (f"{N} stores in total !!")

# 2) ページング取得
shops = []
for start in range(1, N+1, 100):
    param ={
        'key': API_KEY,
        'large_area': 'Z011',
        'format': 'json',
        'count': 100,
        'start': start
    }
    while True:
        try:
            res = requests.get(BASE, params=param, timeout=(3,60) ,stream=True)
            data = res.json()['results']['shop']
            for dic in data:
                processed=parse_shop_info(dic)
                #print (processed,"\n")
                if not processed: break
                shops.append(processed)
            
            print (f"{start}/{N} done")
            break
        except:
            print ("TRYING AGAIN")
            continue
             
  
    


    

print(f'Fetched {len(shops)} shops (expected {N})')
df = pd.DataFrame(shops)
#print (shops)
csv_file = "hotpepper_data.csv"
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f'CSV saved: {csv_file}')