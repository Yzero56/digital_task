from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def page1():
    return render_template('page1.html')

@app.route('/compare')
def page2():
    with open("product_compare.json",'r',encoding='UTF-8') as f:
        data = json.load(f)
    
    my_cpu = {}
    with open("my_cpu_fn.txt",'r',encoding="UTF-8") as f:
        for line in f:
            line = line.strip() #각 줄마다 앞뒤에 공백, 줄바꿈 문자가 있을 수 있음 -> 각 줄을 처리할 때마다 공백을 제거하는 것이 좋음.
            if ':' in line:
                key, value = line.split(":", 1) #:기준으로 나누기 , 한번만 나누기 
                my_cpu[key.strip()] = value.strip()
    
    return render_template('page2.html', data=data, my_cpu=my_cpu)       

if __name__ == '__main__': #현재 스크립트 파일이 프로그램의 시작점이 맞는지 판단하는 작업. 즉, 스크립트 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도!
    app.run(debug=True)