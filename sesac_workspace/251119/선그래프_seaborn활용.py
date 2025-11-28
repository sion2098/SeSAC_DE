# import matplotlib.pyplot as plt
# import seaborn as sns
# plt.rcParams['font.family'] ='Malgun Gothic'
# plt.rcParams['axes.unicode_minus'] = False

# year = [2018, 2019, 2020, 2021, 2022, 2023]
# python = [5.8, 8.17, 9.31, 11.87, 15.63, 14.51]
# C = [13.59, 14.08, 16.72, 14.32, 12.71, 14.73]
# java = [15.78, 15.04, 16.73, 11.23, 10.82, 13.23]
# JS = [3.49, 2.51, 2.38, 2.44, 2.12, 2.1]


# # seaborn 선 그래프 함수
# sns.set_style("darkgrid")
# sns.lineplot(x=year, y=python, label="Python") #seaborn은 legend() 호출하지 않아도 범례 사용 가능
# sns.lineplot(x=year, y=java, label="JAVA")
# plt.show()

# 월별 데이터 시각화를 위해 데이터 그룹화 후, 수치형 컬럼에 대한 평균 구하기
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("251119/seoul_park.csv") # 데이터셋 읽어오기

group_month = df.groupby('월') # 월 컬럼으로 그룹화 진행
df_mon = group_month.mean(numeric_only=True) # 그룹마다 수치형 컬럼에 대해 평균을 구함(월별 수치형 컬럼들의 평균)
print(df_mon)

plt.title("서울대공원 입장객 분석")
# plt.plot(df_mon['어른'], label='어른', marker="o", linestyle="--", color="skyblue") # 그룹화한 dataframe df_mon에서 '어른' 컬럼 추출 #월별 어른 입장객 수의 평균
# plt.plot(df_mon['어린이'], label='어린이', marker=".", linestyle="-.", color="pink") #월별 어린이 입장객 수의 평균
# plt.plot(df_mon['청소년'], label='청소년', marker = "^", linestyle=":", color="violet") #월별 청소년 입장객 수의 평균
plt.xlabel('월')
plt.ylabel('입장객 수')
plt.xticks(range(1,13)) #x축 눈금 조절
plt.legend() # 범례 추가
plt.grid(True, axis='x')
# plt.show()



# data: 대상 데이터프레임
# x: 그 데이터프레임에서 x축에 넣을 컬럼의 "이름"
sns.lineplot(data=df, x='월', y='어른', errorbar=None) #errorbar=None 전달 시, 자동으로 나오는 오차 영역/막대 등 삭제
plt.show()