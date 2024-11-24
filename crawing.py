import requests
from bs4 import BeautifulSoup
import pandas as pd 
import json

URL = "https://www.intel.co.kr/content/www/kr/ko/products/compare.html?productIds=236847,240961,241060,240958,240956,241062,241063,240957,240954,241066,241067,240951,240959,240955,240960"
response = requests.get(URL)

html = response.text
soup = BeautifulSoup(html, "html.parser") 
#print(response.status_code)

#링크 출력 
link = []
complete_link = []
items = soup.find_all('a', class_ = "ark-accessible-color")
#print(items)

for item in items:
    save = item.get('href')

    if save:
        link.append(save)

unique_task = list(dict.fromkeys(link)) #순서대로 중복 살피기  #set: 순서 신경 안씀. 

filter_task = []
for url in unique_task:
    if "/specifications.html" in url:
        filter_task.append(url)
 
complete_link.extend(filter_task)

print(f"제거 전: {len(link)}")
print(f"제거 후: {len(filter_task)}")

index = 1
for v_complete_link in complete_link: #1. 인덱스 제공 2. 리스트항목 반환 
    print(f"인덱스: {index}, 링크: {v_complete_link}")
    index += 1

 
#collection 출력 link와 같은 index 공유 
name = []
for name_v in items:
    name_v_v = name_v.get_text(strip = True) #반드시 텍스트 처리할 것!!! 
    if "Intel® Core™" in name_v_v:
        if "Intel® Core™ Ultra processors (Series 1)" in name_v_v:
            continue
        name.append(name_v_v)

unique_name = list(dict.fromkeys(name))


    
for i in unique_name:
    print(i)

index = 1
for collection in unique_name:  #1. 인덱스 제공 2. 리스트항목 반환 
    print(f" 인덱스: {index}, 제품명: {collection}")    
    index += 1
    
#data에 저장 후 JSON으로 변경 
data = []

core = soup.find_all('td',{'data-key':'CoreCount'})
thread = soup.find_all('td',{'data-key':'ThreadCount'})
max_hz = soup.find_all('td',{'data-key':'ClockSpeedMax'})
origin_hz = soup.find_all('td',{'data-key':'PCoreBaseFreq'})

    
for collection, core_count, thread_num, max_hz_v, origin_hz_v, v_complete_link in zip(unique_name, core, thread, max_hz, origin_hz, complete_link):
    
    core_text = core_count.get_text(strip = True) if core_count else ''
    thread_text = thread_num.get_text(strip = True) if thread_num else ''
    max_hz_text = max_hz_v.get_text(strip = True) if max_hz_v else ''
    origin_hz_text = origin_hz_v.get_text(strip = True) if origin_hz_v else ''
    
    products_dic = {
        "제품명"  : collection,
        "코어 수" : core_text,
        "스레드 수" : thread_text,
        "최대 터보 주파수" : max_hz_text,
        "Performance-core 기본 주파수" : origin_hz_text,
        "링크" : v_complete_link, #리스트 아니어서 가능한듯! 
    }
    
    data.append(products_dic)
        

with open("product_compare.json",'w',encoding='UTF-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4 ) #들여쓰기: 4
    #print(data)

#json 파일 읽어서 표 형식으로 정렬하기
with open('product_compare.json','r',encoding = 'UTF=8') as f:
    read_data = json.load(f)
    
df = pd.DataFrame(data, columns = ["제품명","코어 수","스레드 수", "최대 터보 주파수", "Performance-core 기본 주파수", "링크"])
print(df)

#엑셀파일로 변환하기 
df.to_excel('compare.xlsx', index = False)


