#1초당 반복해서 정보를 출력하는 코드 만들기
import psutil
import cpuinfo
import schedule 
import time 
import threading
#from queue import Queue

curr_sent = 0
curr_recv = 0

prev_sent = 0
prev_recv = 0


#나의 CPU 정보 출력하기 
def my_cpu_load():
    
    print("스레드1 시작")
    #cpu 제품명
    cpu_info = cpuinfo.get_cpu_info()
    m = cpuinfo.get_cpu_info()['brand_raw']
    
    #cpu의 현재 주파수 출력하기 = 속도
    cpu = psutil.cpu_freq()
    cpu_current_ghz = round(cpu.current / 1000, 2) #round함수: (number, 소수점 반올림)
    
    #cpu의 물리코어 수(동시에 몇개의 일을 처리할 수 있는가?)
    cpu_core = psutil.cpu_count(logical=False)
    
    my_cpu = (f"CPU 모델명: {m}\n"
              f"CPU 속도: {cpu_current_ghz}GHz\n"
              f"코어 수 : {cpu_core}개\n")
    
    with open("my_cpu_fn.txt",'w', encoding='UTF=8') as f:
        f.write(my_cpu)   

        
def log_system_info():
    global curr_sent, curr_recv, prev_recv, prev_sent
    print("스레드2 시작")
    
    #cpu 제품명
    cpu_info = cpuinfo.get_cpu_info()
    m = cpuinfo.get_cpu_info()['brand_raw']
    
    #cpu 사용량
    cpu_p = psutil.cpu_percent(interval = 1)

    #cpu의 현재 주파수 출력하기 = 속도
    cpu = psutil.cpu_freq()
    cpu_current_ghz = round(cpu.current / 1000, 2) #round함수: (number, 소수점 반올림)

    
    #cpu의 물리코어 수(동시에 몇개의 일을 처리할 수 있는가?)
    cpu_core = psutil.cpu_count(logical=False)
 
    
    #메모리
    memory = psutil.virtual_memory()
    memory_avail = round(memory.available / 1024**3, 1)
    memory_total = round(memory.total/1024**3, 1)

    #보내기
    #네트워크를 통해 보내고 받은 데이터의 크기를 MB단위로 출력, 보내고 받은 데이터: 이전 데이터 양 빼줌으로써 누적되지 않도록 함. 
    net = psutil.net_io_counters()
    curr_sent = net.bytes_sent/1024**2
    curr_recv = net.bytes_recv/1024**2

    sent = round(curr_sent - prev_sent, 1)
    recv = round(curr_recv - prev_recv, 1)
    
    prev_recv = curr_recv
    prev_sent = curr_sent
    
    log_info = (f"CPU 모델명: {m}\n"
                f"CPU 속도: {cpu_current_ghz}GHz\n"
                f"코어: {cpu_core}개\n"
                f"CPU 사용량: {cpu_p}%\n"
                f"사용가능한 메모리: {memory_avail}GB\n"
                f"전체 메모리: {memory_total}GB\n"
                f"보내기: {sent}MB 받기: {recv}MB\n"
                f"\n")
    

    with open("log_system_file.txt",'a', encoding="utf-8") as f:
        f.write(log_info)
        print(f"CPU 모델명: {m}")
        print(f"CPU 속도: {cpu_current_ghz}GHz")
        print(f"코어: {cpu_core}개")
        print(f"CPU 사용량: {cpu_p}%")
        print(f"사용가능한 메모리: {memory_avail}GB")
        print(f"전체 메모리: {memory_total}GB")
        print(f"보내기: {sent}MB 받기: {recv}MB")

def schedule_info():    
    #나의 컴퓨터 정보 10s마다 생성하기 
    schedule.every(5).seconds.do(log_system_info)

    while True: 
        schedule.run_pending() #.run_pending(): 실행할 작업이 있는지를 확인하는 함수
        time.sleep(0.3)  
    

    
if __name__ == '__main__':
    
    t1 = threading.Thread(target=my_cpu_load, args=()) #args= target에 지정된 함수를 받는 인수 
    t2 = threading.Thread(target=log_system_info, args=())
    t1.start()
    t2.start() 
    
    #t1, t2가 모두 실행된 후에 t3 실행하기 
    t3 = threading.Thread(target=schedule_info, args=())
    t3.start()