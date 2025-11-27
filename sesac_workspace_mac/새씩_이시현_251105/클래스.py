'''
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def walk(self):
        print(f"{self.name}이 걷습니다.")

    def eat(self, food):
        print(f"{self.name}이 {food} 를 먹습니다.")

gildong = Person("Gildong", 22)
john = Person("John", 40)

gildong.walk()
john.eat("Banana")


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)

print(p1.name, p1.age)

print(p1)



class Car:    # Car라는 Class 정의
    def __init__(self, name, speed):   
        self.name = name             # 생성자로부터 name 속성을 정의
        self.speed = speed           # 생성자로부터 speed 속성을 정의

    def get_name(self):
        return self.name

    def get_speed(self):
        return self.speed

   

audi = Car("Audi", 10)  # Car 클래스를 바탕으로 객체(audi) 생성
bmw = Car("BMW", 30)    # Car 클래스를 바탕으로 객체(bmw) 생성

print(f"{audi.name}'s speed is {audi.speed}")
print(f"{bmw.name}'s speed is {bmw.speed}")



# Person 클래스 선언
# 생성자로부터 name과 age 속성 정의
# walk와 eat 메서드 정의
# gildong, john 객체 생성

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        print(f"{self.name}이 걷습니다.")
    
    def eat(self,food):
        print(f"{self.name}이 {food}를 먹는다")


gildong = Person("Gildong", 30)
john = Person("John", 55)

gildong.walk()
john.eat("banana")

'''

'''
class Boong:
    def __init__(self, filling, amount):
        self.filling = filling
        self.amount = amount
    
    def put(self):
        return self.filling

    def control(self):
        return self.amount
    
redbean = Boong("팥", "보통")
cream = Boong("슈크림", "많이")
sweet = Boong("고구마", "적게")

print(f"속재료: {redbean.filling} \n속의 양: {redbean.amount}")
print(f"속재료: {cream.filling} \n속의 양: {cream.amount}")
print(f"속재료: {sweet.filling} \n속의 양: {sweet.amount}")

'''