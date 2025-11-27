'''
# i가 양수인 동안 반복
# i가 0이면 반복문 종료
i = 5

while i > 0:
    print(i)
    i -= 1  # i = i - 1
print("while문 종료")



i = 1
while i < 20:
    print(f"9 x {i} = {9*i}")
    i += 1
print("구구단 끝")


#계좌 잔액이 인출할 금액보다 클 때까지 인출하기
balance = 10000 #초기 잔액
withdraw = 1500 #인출 금액

while balance >= 1500:
    print(f"현재 잔액: {balance}")
    print(f"{withdraw}원 인출")
    balance -= withdraw
    print(f"잔액 {balance}원")
print(f"인출 종료. 최종 잔액: {withdraw}")



#원하는 값 리스트에서 탐색하기
numbers = [4, 2, 5, 6, 9, 8, 10, 5]
target = 12
i = 0

while i < len(numbers):  # i < 6
    if numbers[i] == target:
        print(f"{i+1}번째에서 {target} 탐색완료")
        break
    i += 1

#원하는 값이 리스트에 없을때 출력 값
if i == len(numbers):
    print("탐색하지 못했습니다.")

'''
'''
while True:
    print("======= 쇼핑몰 메뉴 ======")
    print("1. 상품 담기")
    print("2. 장바구니 보기")
    print("3. 결제하기")
    print("4. 종료하기")

    choice = input("메뉴 선택: ")

    if choice == "1":
        # 상품 담기

    elif choice == "2":
        # 장바구니 보기
    
    elif choice == "3":
        # 결제하기
    
    elif choice == "4":
        print("프로그램 종료")
        break
    else:
        print("잘못된 입력입니다. 1~4 중에서 선택하세요.")

        '''