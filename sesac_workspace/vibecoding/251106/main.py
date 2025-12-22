import cal   #생성한 cal 모듈 불러오기
import datetime 

print(dir(cal))

# 3,4 값을 cal 모듈에 있는 plus 함수를 사용해 계산 후 결과값 출력
print(cal.plus(3,4))

# cal 모듈에 있는 변수 var1 값을 불러와 출력
print(cal.var1)

# cal 모듈에 있는 Person 클래스 사용
p = cal.Person("Gildong",30)  # 객체 p를 생성해 name, age 값을 Person 클래스의 생성자 한번 돌림
print(p.name, p.age)    # 생성자 돌린 객체 p의 name, age 값을 출력


now = datetime.datetime.now()
print("현재 시각:", now)

today = datetime.date.today()
print("오늘 날짜:", today)