'''
total = 0
for i in [1, 3, 5]:
    total += i  #total = total + i
print(total)


count = 0
for i in [1,2,3,4,5]:
    count += 1  #count = count + 1
    print(count)
print(count)

total = 0
seq = [1, 3, 5, 7, 9]
for i in seq:
    print(f"현재 원소: {i}")
    total += i  #total = total + i
    print(f"현재 원소와 더한 값: {total}")
print(f"최종 결과: {total}")  #반복문에 종속되지 않음(들여쓰기X)


#가격 목록에 각각 할인율 적용한 가격 출력
prices = [1000, 2500, 8000, 15000]
discount_ratio = 0.9
for price in prices:
    #print(int(price * discount_ratio))
    print(f"{price}의 할인된 가격은 {int(price*discount_ratio)}입니다")


#반복문으로 num_list 리스트에 값 추가
num_list = [1]
for i in range(2,5): #i에 2가 저장되어 num_list에 i값 추가됨
    num_list.append(i)
print(num_list)


count = 0
for i in range(10):
    count += 1
print(count)


for i in range(5, 10): # b-a번 반복
    print(i)

print("---------")

for i in range(5): # 0 ~ 5미만 (= a번 반복)
    print(i)

print("---------")

for i in range(5, 10, 2): 
    print(i)



for i in range(1,11):
    mul = 2 * i
    print(f"2 곱하기 {i}는 {mul} 입니다.")



num_list = [3, 4, 1, 5, 2]
# print(len(num_list))  -> 출력값 5
for i in range(len(num_list)):  # range(len(num_list)) = range(5) = range(0, 5) = 0부터 4까지 -> 인덱스로 사용
    print(i, num_list[i])  # i는 인덱스 값, num_list[i]는 리스트에 해당하는 인덱스 값은 인덱싱해서 가져온 것임



str_var = "Hello Python"

for i in range(len(str_var)):
    #len(str_var) = 12
    #range(12) -> 0부터 12미만
    #각 값을 i에 저장
    print(i, str_var[i])



student = ["시온", "리쿠", "유우시", "재희", "료", "사쿠야"]

for i in range(len(student)):
    print(f"출석번호 {i}번은 {student[i]} 입니다.")



prices = [3000, 4500, 10000, 8000, 22000]
quantities = [3, 4, 1, 2, 1]

total = 0
for i in range(len(prices)):
    total += prices[i] * quantities[i]
    product_total = prices[i] * quantities[i]
    print(f"{i+1}번째 제품의 총 금액은 {product_total}")
print(f"모든 제품의 총 금액은{total}입니다")



#상품의 가격이 10000원 이상인 상품에 대해서만 10% 할인 적용
#새로 계산된 상품 가격을 discounted 리스트에 추가하기

prices = [4000, 25000, 7500, 12000, 18500]
discounted = [ ]

for i in range(len(prices)):
    if prices[i] >= 10000:
        discounted.append(int(prices[i] * 0.9))
    else:
        discounted.append(prices[i])
print(f"할인 적용된 후의 가격 리스트는 {discounted}입니다")



#홀수 값만 출력
for i in range(1,11):
    if i % 2 == 0:
        continue
    print(i)
'''

student = ["시온", "리쿠", "유우시", "재희", "료", "사쿠야"]

for i in range(len(student)):
    print(f"출석번호 {i+1}번은 {student[i]} 입니다.")