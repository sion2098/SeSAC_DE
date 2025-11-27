'''
# 튜플 실습
tp = (4, 5, 1, 5, 6)

print(tp[1])  # 인덱싱
print(tp[1:4])  # 슬라이싱
print(6 in tp)  # in 연산자
print(len(tp)) # len() 함수 사용

tp.append(7)  # 데이터 추가 불가능
tp.remove(5)  # 데이터 삭제 불가능
tp[2] = 15  # 데이터 변경 불가능

tp2 = ("아몬드", "일반", "누드", "크런키")  
print(tp + tp2)  # 데이터 이어붙이기(새로운 튜플 생성)
print(tp*3)  # 데이터 반복


#언패킹!
a, b, c, d = (1, 2, 3, 4)  # a/b/c/d 각 변수에 1/2/3/4 각각의 값을 할당한다
print(a)
print(b)
print(c)
print(d)

'''
'''
result = input().split()
print(result)

a, b, c, d = input().split()
print(a, b, c, d)
print(type(a))
print(type(d))


a, b, c, d, e = list(map(int, input().split()))
print(a, b, c, d, e)
print(type(a))



x, y, z = map(int, input().split())
print(x, y, z)
print(type(x), type(y), type(z))



a, b, c = [10, 20, 30]
print(a, b, c)



a, b, c = input().split()
print(a, b, c)
print(type(a))

x, y, z = map(int, input().split())
print(x, y, z)
print(type(x), type(y), type(z))
'''

text = "바나나, 사과, 딸기, 자몽, 귤"
result = text.split(",")
print(result)
