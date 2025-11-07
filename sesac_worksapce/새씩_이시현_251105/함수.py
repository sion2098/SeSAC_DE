'''
# 사칙연산 계산기 함수 만들기
# def 함수명(매개변수1, 매개변수2)
#       함수 body
def add(num1, num2, num3, num4):
    return num1 + num2 + num3 + num4

def sub(num1, num2, num3, num4):
    return num1 - num2 - num3 - num4

def mul(num1, num2, num3, num4):
    return num1 * num2 * num3 * num4

def div(num1, num2, num3, num4):
    return num1 / num2 / num3 / num4

#함수 호출 => 함수이름(인자, 인자)
print(add(3,5,7,9))
print(sub(10,7,95,40))
print(mul(4,6,100,123))
print(div(5000,20,1,1))



#사용자 정의 함수
def hello(x):
    y = 10 * x + 2
    return y

print(hello(10))
print(type(hello(10)))


def formular(a, b):
    c = (a**2) + (b**2)
    print("return:", c)

#formular(2,4)

#result = formular(2,4)
print("result:" , formular(2,4))


def formular(a, b):
    c = (a**2) + (b**2)
    return c

formular(2,4)

result = formular(2,4)
print("result:" , result)



#가변 매개변수 
kor, eng, mat, sci = 98, 77, 85, 90

def max_score(*score):
    return max(score)
print(max_score(kor, eng, sci))
print(max_score(eng, mat, sci))
print(max_score(sci, mat))



def sum_score(kor, eng, math = 80):
    return kor + eng + math

print(sum_score(70, 80, 90))
print(sum_score(70, 80))
print(sum_score(kor = 70, eng = 100))


def unpacking(a,b,c):
    print(a)
    print(b)
    print(c)

mylist = [10, 20, 30]
mytuple = (10, 20, 30)
unpacking(*mylist)
print("----------------")
unpacking(*mytuple)



def three(x):
    return x, x**2, x**3

a, b, c = three(3)
print(a,b,c)


def func1(n1, n2):
    result = n1 + n2
    return result

var1 = 15
var2 = 20
answer = func1(var1, var2)
print(answer)
'''



#print("-------------------------------------")
