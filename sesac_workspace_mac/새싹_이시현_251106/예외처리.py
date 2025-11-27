'''try:     # 예외가 발생할 가능성이 있는 코드 작성
    result = 100 / 2  # 오류 발생! -> 하단의 코드 실행 X
    print(result)
except ZeroDivisionError as e:   # 예외 발생 시 처리할 동작 정의 #ZeroDivisionError : 어떤 예외인지 명시
    print("0으로 나눌 수 없습니다.", e)  

print("Hello")'''

'''#FileNotFoundError

try : 
    f = open("새싹_이시현_251106/text_creat22.txt", encoding = 'utf-8')

except FileNotFoundError as e:
    print("파일을 찾을 수 없습니다", e)
'''

'''# ValueError
# 함수의 매개변수 등 잘못된 값이 전달될 때 발생

try: 
    num = int('')
    print("정수로 변환하면:", num,"입니다")

except ValueError as e:
    print('정수로 변환할 수 없습니다:',e)'''

'''#IndexErro
#리스트나 튜플에 존재하지 않는 인덱스를 접근할 때 발생

try:
    data = [1, 2, 3]
    #print(data[5])
    print(len(data))

except IndexError as e:
    print("인덱스가 범위를 벗어났습니다:",e)'''

'''while True:
    try:
        number = int(input("숫자를 입력하세요:"))
        break

    except ValueError as e:
        print("[Error] 숫자를 입력해주세요!")

print(number)'''
  

'''try:
    a, b = map(int, input("두 정수를 입력하세요:").split())

except ValueError: # 예외 발생 시 동작
    print('입력이 옳지 않습니다')

except Exception:  #Exception은 최상위 예외 클래스라 사용 시 except 중 마지막 except에 작성해야 함
    print('알 수 없는 오류 발생')

else:  # 예외 미발생 시 동작
    print(a + b)

finally:  #예외 상관없이 항상 실행
    print('프로그램 실행을 마쳤습니다.')'''

try:
    my_list=[1,2,3,4,5]
    a, b = map(int, input("두 정수를 입력하세요:").split())
    print(my_list[b])

except ValueError: # 예외 발생 시 동작
    print('[Error] 유효하지 않은 입력입니다!')

except IndexError: 
    print('[Error] 인덱스 범위를 초과했습니다!')

except Exception:  #Exception은 최상위 예외 클래스라 사용 시 except 중 마지막 except에 작성해야 함
    print('[Error] 예기치 못한 오류가 발생했습니다')

else:  # 예외 미발생 시 동작
    print(f"a+b= {a + b}")

finally:  #예외 상관없이 항상 실행
    print('실행을 마쳤습니다.')