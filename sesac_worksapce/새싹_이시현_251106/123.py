while True:
    pass
    try:
        a = int(input("숫자 1입력: "))
        b = int(input("숫자 2입력: "))
        operator = input("연산자 입력 (+, -, *, /)")

        if a == 'q' or b =='q'or operator == 'q':
            break
        
        if operator == '+':
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == '*':
            result = a * b
        elif operator == '/':
            result = a / b

        print(f"결과: {a} {operator} {b} = {result}")

    except ValueError:
        if a == 'q' or b =='q'or operator == 'q':
            break
        print("[오류] 숫자를 입력해주세요.")

    except ZeroDivisionError:
        print("[오류] 0으로 나눌 수 없습니다.")