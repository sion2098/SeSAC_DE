'''
num_list = [10, 20, 30, 40, 50]
print(num_list[2])

str_var = "Python"
print(str_var[3])

wish = ["Sion", "Yushi", "Riku", "Jaehee", "Ryo", "Sakuya"]
print(wish[5])

color = "Bring out the color 내 맘대로"
print(color[20])

wish[2] = "maeda riku"
print(wish)

wish[0] = "Sion 01"
wish[1] = "Yushi 45"
wish[2] = "Riku 03"
wish[3] = "Jaehee 13"
wish[4] = "Ryo ??"
wish[5] = "Sakuya 39"
print(wish)

color [0] = "b"
print(color)

a = "Hello"
print(a[-1])

b = [10, 20, 30, 40, 50]
print(b[-1])
print(b[-2])
print(b[1:-3])
print(a[ :3])
print(b[ :3])
print(b[1: ])

title = "baby blue"
age = [24, 23, 22, 21, 19, 19]
print("E" in title)
print("b" in title)
print("y b" in title)
print(26 in age)
print(19 in age)

title2 = "color"
age2 = [26]
print(title + title2)
print(title + " " + title2)
print(age + age2)
print(age[1:4])
print(len(title2))
print(len(title2[2:7]))
print([24, 23] in age)

print(age)
print([24, 23] in age)
print([24, 23, 22, 21, 19, 19] in age)

nested = [[1,2,3],[4,5,6],[7,8,9]]
len(nested)
len(nested[0])
print((nested[0][2]))
print(nested[2][2])

nested[0][0] = 0
print(nested)
nested[2][0] = "t"
print(nested)


age = [[24, 23, 22, 21, 19, 19]]
print([24, 23] in age)
print([24, 23, 22, 21, 19, 19] in age)


a = [4, 3, 2, 5, 1]

a.append(100)
a.append([3,4,5])
a.append([3,"점심","써브웨이"])
a.append("퇴근")
print(a)
len(a)
len(a[6])

a = [1, 2, 3, 5]
a.insert(3,4)
a.append(6)
a.append(10)
a.insert(3,4)
a.append([7,8,9])
a[-1].insert(2,8.7)
print(a)

num_list = [3,1,2,3]
num_list.remove(3)
print(num_list)
num_list.remove(4)
print(num_list)

num_list.append(6)
num_list.remove(3)
print(3 in num_list)
print(num_list)
print(num_list.pop(1))
num_list.insert(2,3)
num_list.remove(3)
print(num_list.pop(5))
print(num_list)

print(num_list.index(3))
print(num_list.index(4))
num_list.append(1)
print(num_list)
print(num_list.index(1))

num_list = [1, 2, 3, 4, 5, 1]
print(num_list.count(1))

a = ["a", "b", "c", "A", "B", "C", "d", "d", "d"]
a.sort()
a.sort(reverse=True)
print(a)

print(a.count("a"))
print(a.count("d"))
print(a.count("F"))

num_list = [4, 2, 3, 1, 5, 9, 7, 8, 10]
num_list.sort()
num_list.sort(reverse=True)
num_list.insert(4,6)
num_list.sort()
print(num_list)

print(num_list)
num_list.clear()
print(num_list)



var1 = 0
if var1 > 0:
    print(var1, "은 양수입니다.")
print("조건문 종료")



r = int(input("반지름의 길이를 입력하세요: "))

if r > 0:
    print("원의 넓이는" , 3.14*r*r)
    print("원의 둘레는" , 2*3.14*r)

else:
    print("구할 수 없는 반지름 입니다.")

    

num = int(input("홀짝 맞추기!"))
if num % 2 == 0:
    print("입력한 숫자는 짝수입니다.")
else:
    print("입력한 숫자는 홀수네여")



id = input("아이디를 입력하세요:")

if id == "abcd":
    print("메인 페이지로 이동")
else :
    print("경고 메시지 출력")



#입력한 점수의 등급 확인하기
grade = int(input("점수를 입력하세요 :"))

if grade >= 90 and grade <= 100:
    print("A등급")
elif grade >= 80 and grade < 90:
    print("B등급")
elif grade >= 70 and grade < 80:
    print("C등급")
elif grade >= 60 and grade < 70:
    print("D등급")
else : 
    print("F등급 입니다.")



#두 숫자가 양수인지 음수인지 출력
num1 = int(input("숫자 1 입력:"))
num2 = int(input("숫자 2 입력:"))

if num1 > 0 and num2 > 0:
    print("두 수는 모두 양수 입니다.")
elif num1 > 0 and num2 < 0:
    print("num1은 양수, num2는 음수 입니다")
elif num1 <0 and num2 >0 :
    print("num1은 음수, num2는 양수 입니다")
else : 
    print("둘 다 음수 입니다.")


# 조건문 아래처럼 작성 가능
if num1 > 0:
    if num2 > 0:
        print("둘다 양수 입니다.")
    else :
        print("num1은 양수, num2는 음수입니다.")
elif num1 < 0:
    if num2 > 0:
        print("num1은 음수, num2는 양수입니다.")
    else : 
        print("둘 다 음수 입니다.")


a = ["H", "8", "e", "l", "l", "o"]
if "h" in a:
    a.remove("h")
else:
    print("h가 없습니다.")

 

word = "Python"
if len(word) > 5:
    print(word*2)
else:
    print(word)



word = input("단어를 입력하세요:")
if  len(word) >= 5 and 'P' in word:
    print(word)
else :
    print("조건에 맞지않는 단어입니다.")

'''
score = int(input("시험 점수를 입력하세요.: "))
attendance = int(input("출석 점수를 입력하세요.: "))

if score >= 70 and attendance >=90:
    print("통과")
elif score >= 70 and attendance < 90:
    print("조건부 통과(출석 미달)")
else :
    print("미흡")