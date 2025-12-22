import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

year = [2018, 2019, 2020, 2021, 2022, 2023]
python = [5.8, 8.17, 9.31, 11.87, 15.63, 14.51]
C = [13.59, 14.08, 16.72, 14.32, 12.71, 14.73]
java = [15.78, 15.04, 16.73, 11.23, 10.82, 13.23]
JS = [3.49, 2.51, 2.38, 2.44, 2.12, 2.1]

# plt.title("파이썬의 언어 점유율", fontsize=20)
# plt.xlabel("연도",fontsize=15)
# plt.ylabel("점유율",fontsize=15)

# # 선 그래프: plot() 함수; 연도에 따른 파이썬 점유율 변화
# plt.plot(year, python) # x축: year, y축: python
# plt.plot(year, C)
# plt.plot(year, java)

# plt.legend(["Python","C","JAVA"]) #볌례 표시

# plt.plot(year, python, label='Python')
# plt.plot(year, C, label='C')
# plt.plot(year, java, label='JAVA')
# plt.legend()

# #여러개의 figure 사용
# fig1 = plt.figure(1, figsize = (4,3)) #ID가 1인 새로운 figure 객체를 생성
# plt.plot(year, python, label='Python') # 현재 선택된 fig1에 선 그래프 그림
# plt.title("fig1") # 현재 선택된 fig1의 제목 설정

# fig2 = plt.figure(2, figsize=(4,3)) #ID가 2인 새로운 figure 객체 생성
# plt.title("fig2") #현재 선택된 fig2의 제목 설정

# plt.figure(1) #현재 도화지를 1번 도화지로 활성화
# plt.plot(year, java, label="JAVA") #현재 선택된 fig2에 선 그래프 그림

# #하나의 도화지(figure) 안에서 공간을 여러개로 나누기 : subplots()
# fig, (ax1, ax2) =  plt.subplots(2,1, constrained_layout=True) # 1행 2열 -> 2개의 공간 나옴(ax1, ax2)
# ax1.plot(year, python) #왼쪽 공간
# ax1.set_title("파이썬 점유율")
# ax1.set_xlabel("연도")
# ax1.set_ylabel("점유율")

# ax2.plot(year, java) #오른쪽 공간
# ax2.set_title("자바 점유율")
# ax2.set_xlabel("연도")
# ax2.set_ylabel("점유율")

fig, (ax1, ax2, ax3) = plt.subplots(1,3, constrained_layout=True)
ax1.plot(year,python)
ax1.set_title("파이썬 점유율")
ax1.set_xlabel("연도")
ax1.set_ylabel("점유율")

ax2.plot(year,java)
ax2.set_title("자바 점유율")
ax2.set_xlabel("연도")

ax3.plot(year,C)
ax3.set_title("C언어 점유율")
ax3.set_xlabel("연도")

plt.show()