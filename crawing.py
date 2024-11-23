import requests
from bs4 import BeautifulSoup
import pandas as pd 
import json
import psutil
import cpuinfo

for i in range(1,16):
    URL = "https://www.intel.co.kr/content/www/kr/ko/products/compare.html?productIds=236847,240961,241060,240958,240956,241062,241063,240957,240954,241066,241067,240951,240959,240955,240960"
    response = requests.get(URL)

    html = response.text
    soup = BeautifulSoup(html, "html.parser") 
    #print(response.status_code)

    data = []

    collections = soup.select("#arkproductcollection-1")
    core = soup.find_all('td',{'data-key':'CoreCount'})
    thread = soup.find_all('td',{'data-key':'ThreadCount'})
    max_hz = soup.find_all('td',{'data-key':'ClockSpeedMax'})
    origin_hz = soup.find_all('td',{'data-key':'PCoreBaseFreq'})

    for collection, core_count, thread_num, max_hz_v, origin_hz_v in zip(collections, core, thread, max_hz, origin_hz):
        
        collection_text = collection.get_text(strip=True) if collection else ''
        core_text = core_count.get_text(strip = True) if core_count else ''
        thread_text = thread_num.get_text(strip = True) if thread_num else ''
        max_hz_text = max_hz_v.get_text(strip = True) if max_hz_v else ''
        origin_hz_text = origin_hz_v.get_text(strip = True) if origin_hz_v else ''

        products_dic = {
            "제품 콜렉션"  : collection_text,
            "코어 수" : core_text,
            "스레드 수" : thread_text,
            "최대 터보 주파수" : max_hz_text,
            "Performance-core 기본 주파수" : origin_hz_text,
        }
        
        data.append(products_dic)
    
with open("product_compare.json",'w',encoding='UTF-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4 ) #들여쓰기(indent): 4
print(data)

#json 파일 읽어서 표 형식으로 정렬하기
with open('product_compare.json','r',encoding = 'UTF=8') as f:
    read_data = json.load(f) 
    
df = pd.DataFrame(data, columns = ["제품 콜렉션","코어 수","스레드 수", "최대 터보 주파수", "Performance-core 기본 주파수"])
print(df)

#엑셀파일로 변환하기 
df.to_excel('compare.xlsx', index = False)



