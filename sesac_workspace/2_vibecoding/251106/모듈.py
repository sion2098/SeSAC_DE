'''import math

print(math.pi)  #원주율
print(math.e)  #자연상수

print(math.sqrt(16))  #제곱근
print(math.pow(2,3))  #거듭 제곱
print(math.ceil(3.1)) #올림
print(math.floor(3.9)) #내림

print(dir(math))  #모듈에 담겨있는 함수,변수 목록 출력'''

'''# 난수(무작위 수)를 생성해주는 random 모듈
import random

print(random.random())   #0 ~ 1 사이 난수
print(random.randint(1,10))  #1 ~ 10 사이 정수 난수
print(random.choice(['가위', '바위', '보']))  # 리스트에서 무작위 선택
print(random.sample(range(1,46), 6))  # 목록에서 k개 샘플 뽑기

print(dir(random))'''

'''# datetime 모듈 / 날짜와 시간을 다룰때 가장 기본적인 모듈
import datetime

now = datetime.datetime.now()  #현재 날짜와 시간
print("현재 시각:", now)

today = datetime.date.today()  #오늘 날짜
print("오늘 날짜:", today)

future = today + datetime.timedelta(days=7)  #시간 차(간격) 계산
print("일주일 뒤:", future)

print(dir(datetime))'''

'''import math

print(math.factorial(5))'''

'''from math import factorial
print(factorial(5))'''

# from datetime import 함수들
from datetime import datetime, date, timedelta
from math import pi, sqrt

now = datetime.now()  #현재 날짜와 시간
print("현재 시각:", now)

today = date.today()  #오늘 날짜
print("오늘 날짜:", today)

future = today + timedelta(days=7)  #시간 차(간격) 계산
print("일주일 뒤:", future)

print(pi)
print(sqrt(16))
#print(ceil(3.9))  #from-import에 포함되지 않아 사용 불가능
