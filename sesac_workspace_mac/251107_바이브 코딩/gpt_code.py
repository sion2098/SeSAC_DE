'''# 숫자 맞추기 게임 🎮 (정답 맞출 때까지 반복)

# 랜덤 모듈 불러오기 (컴퓨터가 랜덤 숫자를 만들 수 있도록 함)
import random

# 1~10 사이의 숫자를 컴퓨터가 하나 정해요
c_num = random.randint(1, 10)

# 도전 횟수를 세기 위한 변수예요
count = 0

# 무한 반복문을 사용해요 (정답을 맞출 때까지 계속)
while True:
    # 사용자에게 숫자를 입력받아요
    u_num = input("1부터 10 사이의 숫자를 맞춰보세요: ")
    
    # 입력받은 값을 숫자로 바꿔줘요
    u_num = int(u_num)
    
    # 도전 횟수를 1 증가시켜요
    count += 1
    
    # 정답인지 확인해요
    if u_num == c_num:
        print("정답입니다!", count, "번만에 성공하셨어요!")
        break  # 정답이면 반복을 멈춰요
    else:
        print("틀렸습니다! 다시 시도해보세요.")'''



'''# 숫자 리스트를 준비해요
numbers = [3, 8, 2, 10, 5]

# 첫 번째 값을 가장 큰 수로 저장해요
max_num = numbers[0]

# 리스트 안의 숫자를 하나씩 꺼내서 비교해요
for num in numbers:
    # 만약 꺼낸 숫자가 max_num보다 크면, max_num을 바꿔요
    if num > max_num:
        max_num = num

# 최종 결과를 출력해요
print("리스트에서 가장 큰 수는", max_num, "입니다.")'''



'''import random  # 랜덤 기능 사용

# 아침(6~11) 인사말 리스트
morning_greetings = [
    "출근하느라 힘들죠? 오늘은 아무도 일을 안시키길 바랄게요!",
    "좋은 아침이에요! 커피 한 잔으로 에너지 충전하세요 ☕",
    "햇살이 눈부신 아침이에요! 오늘 하루도 파이팅 💪",
    "벌써 아침이라니... 하지만 당신은 멋지게 해낼 거예요!",
    "오늘도 출근길에 좋은 일만 가득하길 바랍니다 🌞"
]

# 오후(12~17) 인사말 리스트
afternoon_greetings = [
    "맛점 했어? 오후 업무 힘내! 잠깐 커피타임 가질까?",
    "점심 먹고 나니 졸리죠? 잠깐 스트레칭 어때요?",
    "오후도 활기차게! 오늘의 절반은 이미 해냈어요 👏",
    "커피향처럼 기분 좋은 오후 되세요 ☕",
    "오늘 일도 멋지게 마무리할 당신을 응원해요!"
]

# 저녁(18~23) 인사말 리스트
evening_greetings = [
    "오늘 하루도 수고했어요! 집에 가서 푹 쉬어요 🏠",
    "퇴근이 코앞이에요! 조금만 더 힘내요 💪",
    "맛있는 저녁 먹고 하루 마무리 잘하세요 🍽️",
    "오늘 하루 잘 버텨냈어요. 대단해요 👏",
    "불금이 아니어도 오늘은 충분히 고생 많았어요!"
]

# 그 외(0~5) 인사말 리스트
night_greetings = [
    "좋은 꿈 꾸고 있나요? RAM수면 드가자 😴",
    "늦은 시간이네요, 푹 쉬고 내일 또 봐요 🌙",
    "이 시간까지 깨어 있다니 대단해요! 얼른 자요 💤",
    "별빛이 예쁜 밤이에요. 좋은 꿈 꾸세요 ⭐",
    "이 밤이 지나면 더 멋진 하루가 올 거예요 🌌"
]

# 프로그램 반복 시작
while True:
    user_input = input("몇시인가요? (0~23 입력 or 'out' 입력 시 종료): ")

    # 1️⃣ out 입력 시 종료
    if user_input.lower() == "out":
        print("프로그램을 종료합니다. 좋은 하루 보내세요 👋")
        break

    # 2️⃣ 숫자 여부 확인
    if not user_input.isdigit():
        print("문구를 확인해주세요.")
        continue

    # 3️⃣ 숫자면 int로 변환
    hour = int(user_input)

    # 4️⃣ 0~23 범위 확인
    if hour < 0 or hour > 23:
        print("시간을 다시 확인해주세요.")
        continue

    # 5️⃣ 시간대에 따라 랜덤 인사말 출력
    if 6 <= hour <= 11:
        print(random.choice(morning_greetings))
    elif 12 <= hour <= 17:
        print(random.choice(afternoon_greetings))
    elif 18 <= hour <= 23:
        print(random.choice(evening_greetings))
    else:
        print(random.choice(night_greetings))'''

'''# Step1: 물건 가격 입력 받기
# input()으로 물건 가격을 입력받고 int()로 형 변환하여 price 변수에 저장
price = int(input("물건은 얼마인가요?:"))

# Step2: 손님이 낸 돈 입력 받기
# input()으로 손님이 낸 금액을 입력받고 int()로 형 변환하여 pay 변수에 저장
pay = int(input("손님이 낸 금액은: "))

# Step3: 거스름돈 계산
# pay - price로 거스름돈을 계산하고, 음수(지불 부족)인 경우 조건 처리
change = pay - price  # 임시 계산값
if change < 0:
    # 지불한 금액이 부족한 경우 부족한 금액을 안내하고 return_price를 0으로 설정
    print(f"지불 금액이 부족합니다. 부족한 금액: {-change}원")
    return_price = 0
else:
    # 거스름돈이 있으면 그 값을 return_price에 저장
    return_price = change

# Step4: 결과 출력
# 계산된 거스름돈을 출력
print(f"여기 거스름돈 ({return_price}) 입니다")'''

'''# ✌️ 가위바위보 게임 ✊✋

import random  # 컴퓨터가 무작위로 선택할 수 있도록 random 불러오기

count = 0  # 시도 횟수를 세는 변수
options = ["가위", "바위", "보"]  # 가능한 선택

# 각 단어에 해당하는 이모지를 딕셔너리(사전) 형태로 저장
emoji = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋"
}

while True:  # 사용자가 이길 때까지 반복
    com = random.choice(options)  # 컴퓨터가 가위/바위/보 중 하나를 랜덤으로 선택
    user = input("당신은 가위/바위/보 중 무엇을 내겠습니까?: ")  # 사용자 입력
    count += 1  # 시도 횟수 1 증가

    # 입력이 올바르지 않은 경우
    if user not in options:
        print("⚠️ 가위, 바위, 보 중에서만 입력해주세요!")
        continue  # 다시 입력받기

    # 컴퓨터와 사용자가 낸 걸 이모지로 보여주기
    print(f"컴퓨터는 {com} {emoji[com]} 를 냈어요!")

    # 비긴 경우
    if com == user:
        print("🤝 컴퓨터와 통했다! 다음번엔 이겨보자 😊")

    # 사용자가 이기는 경우
    elif (user == "가위" and com == "보") or (user == "바위" and com == "가위") or (user == "보" and com == "바위"):
        print(f"🎉 당신은 {count}번만에 {user} {emoji[user]} 로 이겼어요! 🏆")
        break  # 게임 종료

    # 컴퓨터가 이기는 경우
    else:
        print("😅 다시한번 도전해봐요!")'''



'''# 비밀번호 강도 검사기 프로그램

# 1. 사용자에게 비밀번호를 입력받기
password = input("비밀번호를 입력하세요: ")

# 2. 비밀번호의 길이를 구해서 length 변수에 저장
length = len(password)

# 3. 비밀번호 안에 숫자가 있는지 확인하기
# any()는 비밀번호의 글자들 중 하나라도 숫자인지 확인해줌
has_number = any(char.isdigit() for char in password)

# 4. 비밀번호가 안전한지 확인하기
# 길이가 8자 이상이고, 숫자가 포함되어 있으면 안전한 비밀번호로 판단
if length >= 8 and has_number:
    print("안전한 비밀번호입니다")
else:
    print("약한 비밀번호입니다")
'''

'''# 출석 체크 프로그램

# 학생 이름을 저장할 리스트
name_list = []

# 출석/결석 여부를 저장할 리스트
attend_list = []

# 총 학생 수 (5명으로 고정)
total_students = 5

# 5명의 학생 정보를 입력받기 위한 반복문
for i in range(total_students):
    # 학생 이름과 출결 현황을 입력받기
    data = input("학생이름과 출결 현황을 작성해주세요 (공백으로 구분): ")
    name, attend = data.split()

    # 이름과 출결을 각각 리스트에 추가
    name_list.append(name)
    attend_list.append(attend)

# ✅ [수정된 부분]
# → 리스트 출력문을 for문 '밖으로' 옮김
# → 5명 입력 후에만 한 번 출력됨
print("\n=== 입력 완료! 전체 명단 출력 ===")
print("이름 목록:", name_list)
print("출결 현황:", attend_list)

# 출석한 학생 수 세기
students = attend_list.count("출석")

# 출석률 계산 (소수점 한 자리까지)
attendance = (students / total_students) * 100

# 최종 결과 출력
print("\n=== 최종 출석 결과 ===")
print("출석 인원수:", students)
print(f"출석률: {attendance:.1f}%")
'''

'''# 단어 빈도수 세기 프로그램

# 1. 사용자에게 문장 입력받기
sentence = input("입력하고 싶은 내용을 한줄 문장으로 입력해주세요: ")

# 2. 입력받은 문장을 공백 기준으로 단어 분리
words = sentence.split()

# 3. 단어 등장 횟수를 저장할 딕셔너리 생성
word_count = {}

# 4. 단어 리스트를 하나씩 꺼내서 빈도수 계산
for word in words:
    # 만약 단어가 딕셔너리에 이미 있다면
    if word in word_count:
        # 기존 값에 1을 더해줌
        word_count[word] += 1
    else:
        # 없다면 처음 등장한 것이므로 1로 설정
        word_count[word] = 1

# 5. 모든 단어와 등장 횟수를 출력
print("\n=== 단어별 등장 횟수 ===")
for w in word_count:
    print(f"{w}: {word_count[w]}번")
'''

'''# BMI 계산기 및 판정 프로그램

# 1. 사용자에게 키(cm)와 몸무게(kg)를 입력받기
# float()을 사용해 소수점 입력도 가능하게 함
height_cm = float(input("키(cm)를 입력하세요: "))
weight_kg = float(input("몸무게(kg)를 입력하세요: "))

# 2. 키를 cm → m로 변환
height_m = height_cm / 100

# 3. BMI 계산 (몸무게 / (키*키))
bmi = weight_kg / (height_m * height_m)

# 4. BMI 값에 따라 판정
if bmi < 18.5:
    result = "저체중"
elif bmi < 23:
    result = "정상"
elif bmi < 25:
    result = "과체중"
else:
    result = "비만"

# 5. 결과 출력 (BMI는 소수점 1자리까지만)
print("\n=== BMI 계산 결과 ===")
print(f"BMI: {bmi:.1f}")
print(f"판정: {result}")'''


# 도서 관리 시스템 3단계 확장: 대여 + 반납 기록 관리
from datetime import datetime  # 날짜와 시간 기록을 위한 모듈

# 1. Book 클래스 정의
class Book:
    def __init__(self, title, author, isbn, stock):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.stock = stock

# 2. 도서 목록 출력 함수
def print_books(book_list):
    print("\n=== 현재 도서 목록 ===")
    for i, book in enumerate(book_list, start=1):
        print(f"{i}. {book.title} (저자: {book.author}, ISBN: {book.isbn}, 재고: {book.stock}권)")

# 3. 대여/반납 기록 저장 리스트
borrow_history = []   # 대여 기록
return_history = []   # 반납 기록

# 4. 대여 기록 추가 함수
def add_borrow_record(title):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    borrow_history.append({'title': title, 'date': now})

# 5. 반납 기록 추가 함수
def add_return_record(title):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return_history.append({'title': title, 'date': now})

# 6. 대여/반납 기록 조회 함수
def show_all_history():
    print("\n=== 대여/반납 기록 조회 ===")

    if not borrow_history and not return_history:
        print("아직 대여나 반납 기록이 없습니다.")
        return

    # 대여 기록 출력
    if borrow_history:
        print("\n[📘 대여 기록]")
        for i, record in enumerate(borrow_history, start=1):
            print(f"{i}. {record['title']} (대여일시: {record['date']})")
    else:
        print("\n[📘 대여 기록] 없음")

    # 반납 기록 출력
    if return_history:
        print("\n[📗 반납 기록]")
        for i, record in enumerate(return_history, start=1):
            print(f"{i}. {record['title']} (반납일시: {record['date']})")
    else:
        print("\n[📗 반납 기록] 없음")

# 7. 도서 대여 함수
def borrow_book(book_list):
    while True:
        title = input("대여할 책 이름: ").strip()
        found = False

        for book in book_list:
            if book.title == title:
                found = True
                if book.stock > 0:
                    book.stock -= 1
                    print(f"'{book.title}' 도서를 대여했습니다.")
                    add_borrow_record(book.title)  # ✅ 대여 기록 추가
                    print_books(book_list)
                else:
                    print(f"'{book.title}' 도서는 현재 재고가 없습니다. (대여 불가)")
                return
        
        if not found:
            print("존재하지 않는 책 제목을 입력했습니다. 다시 입력해주세요.")

# 8. 도서 반납 함수
def return_book(book_list):
    while True:
        title = input("반납할 책 이름: ").strip()
        found = False

        for book in book_list:
            if book.title == title:
                found = True
                book.stock += 1
                print(f"'{book.title}' 도서를 반납했습니다.")
                add_return_record(book.title)  # ✅ 반납 기록 추가
                print_books(book_list)
                return
        
        if not found:
            print("존재하지 않는 책 제목을 입력했습니다. 다시 입력해주세요.")

# 9. 초기 도서 목록 (예시 데이터)
books = [
    Book("파이썬 완전 정복", "김코딩", "9781234567890", 3),
    Book("인공지능 입문", "이자바", "9780987654321", 2),
    Book("데이터 분석의 모든 것", "박데이터", "9781111222233", 1),
    Book("코딩 인터뷰 마스터", "정엔지니어", "9784444555566", 4),
    Book("알고리즘 트레이닝", "최수학", "9789999888877", 0)
]

# 10. 프로그램 메인 루프
while True:
    print("\n=== 도서 대여 시스템 ===")
    print("원하는 서비스를 입력하세요")
    print("1. 대여")
    print("2. 반납")
    print("3. 종료")
    print("4. 대여/반납 기록 조회")

    try:
        service = int(input("번호 입력: "))

        if service == 1:
            print_books(books)
            borrow_book(books)
        elif service == 2:
            print_books(books)
            return_book(books)
        elif service == 3:
            print("프로그램을 종료합니다.")
            break
        elif service == 4:
            show_all_history()
        else:
            print("1, 2, 3, 4 중 하나를 입력해주세요.")
    except ValueError:
        print("숫자로 입력해주세요.")


