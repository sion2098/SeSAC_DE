'''
print("---------------------------------------")

# person이라는 딕셔너리 생성
# 한 딕셔너리 안에 동일한 키 사용 불가능 -> 값 덮어씌움 당함
person = {"name":"김개똥", 
          "age":24, 
          "address":"서울시 성동구",
          "phone_number" : "010-1234-5678",
          "email" : "wish@gmail.com",
          "name":"이시현", 
          "age":26, 
          "address":"서울시 중구",
          "phone_number" : "010-9876-5432",
          "email" : "lsh@gmail.com"
        }

print(person)  # 생성한 딕셔너리 출력
print(person["name"])


person = {"name":"오시온", 
          "age":24, 
          "address":"서울시 성동구",
          "phone_number" : "010-1234-5678",
          "email" : "wish@gmail.com",
          }

print(person)

# key로 value 불러오기
print(person["name"])

# 새로운 key 추가
person["gender"] = "M"
print(person)

# 기존 키의 value 수정하기
person["gender"] = "Angel"
print(person)

# 삭제하기
del person["address"]
print(person)

"address" in person
"gender" in person



# 딕셔너리에 key:value 포함 여부 확인(in 연산자 사용)
group = {"name" : "이시현",
         "age" : 26,
         "gender" : "F"}

print(group)

if "name" in group:
    group["name"] = "마에다"
print(group)


~~~ 'low' in level 확인 필요
level = {'low' : 1,
         'medium' : 5
        }

# level 에서 'medium' 값 가져오기
print(level["medium"])

# level에서 'low' 키가 있는지 확인하기
'low' in level

# level에 {'high' : 10} 추가하기
level["high"] = 10
print(level)

# level에 'low' 키 삭제하기
del level['low']
print(level)



company = { 
    "name" : "ABC Corp",
    "departments" : {
        "HR" : {
            "manager" : "이영희",
            "employees" : ["홍길동", "김민수"]
        },
        "IT" : {
            "manager" : "박지훈",
            "employees" : ["최수빈", "이시현", "이서연"]
        }
    }
}

print(company)
print(company["departments"]["HR"]["manager"])

# IT 부서의 직원 수를 가져오고 싶다
print(len(company["departments"]["IT"]["employees"]))



dict = {
    'Korea' : 'Seoul',
    'Vietnam' : 'Hanoi',
    'Japan' : 'Tokyo'
}

#print(dict.keys())
#print(dict.values())
#print(dict.items())

for x in dict:   # dict = dict.keys()와 같은 의미
    print(x)

print("---------------------")

for y in dict.values():
    print(y)


dict = {
    'Korea' : 'Seoul',
    'Vietnam' : 'Hanoi',
    'Japan' : 'Tokyo'
}

for x, y in dict.items():
    print(x,y)
    print(x)
    print(y)



# dict() 함수 사용 -> 다중 원소로 구성된 리스트/튜플을 딕셔너리로 변환
info1 = {
    'name' : '길동',
    'year' : 1999
         }

li = [('name','길동'), ('year', 1999)]  # 내부 리스트(or 튜플)의 원소가 두개여야 함

info2 = dict(li)
print(info2)


'''

# names와 scores라는 각각 빈 리스트 정의 후 5명의 학생 이름과 점수를 입력받아 각 리스트에 저장
# 이 두개의 리스트를 활용해 딕셔너리 생성

names = [ ]
scores = [ ]

for i in range(5):
    names.append(input("이름을 입력하세요: "))
    print(names)   # 입력값 추가할 때마다 리스트에 저장된 값 출력하기
    scores.append(int(input("점수를 입력하세요: ")))
    print(scores)  # 입력값 추가할 때마다 리스트에 저장된 값 출력하기

print(dict(zip(names, scores)))


'''

names = [ ]
scores = [ ]

for i in range(5):
    n = input("이름을 입력하세요: ")
    s = int(input("점수를 입력하세요: "))
    names.append(n)
    scores.append(s)

result = dict(zip(names, scores))
print(result)

# input().split() 사용해서 작성해보기

'''