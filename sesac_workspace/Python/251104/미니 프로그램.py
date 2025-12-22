who = { }
vote = 0
none = 0
for i in range(3):
    name = input("후보자 입력: ")
    who[name] = vote
print(who)

for i in range(10):
    name2 = input("누구: ")
    if name2 in who:
        who[name2] += 1
    else:
        none += 1

print("==== 투표 결과 ====")
print(f"총 투표자: 10명")
print(f"유효 튜표: {10-none}명")
print(f"무효 튜표: {none}")

print("==== 후보별 득표 현황 ====")
for x, y in who.items():
    print(f"{x}: {y}표")

print("==== 당선자 발표 ====")
for x,y in who.items():
    if y == max(who.values()):
        print(f"{x} 후보가 당선되었씁니다! (득표수: {y}표)")
        break
