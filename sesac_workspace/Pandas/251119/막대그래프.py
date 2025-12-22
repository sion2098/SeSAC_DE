import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("251119/seoul_park.csv")

#요일별 시각화
#요일별 그룹화 후, 숫자형 데이터에 대해 평균 구함
df_week = df.groupby('요일').mean(numeric_only=True)
#print(df_week)
#인덱스에 있는 '요일' 정보를 새 컬럼으로 추가(=인덱스 초기화)
df_week = df_week.reset_index()  #drop 없이 reset_index 사용하면 기존 인덱스가 새로운 컬럼으로 추가됨

# 데이터 정렬된 데이터프레임 새로 생성
df_sorted = df_week.sort_values('청소년')
plt.title('서울대공원')
# plt.bar(df_week['요일'], df_week['청소년']) #세로 막대
# plt.barh(df_week['요일'], df_week['청소년']) #가로 막대
# plt.barh(df_sorted['요일'], df_sorted['청소년']) #가로 막대(정렬된 ver)
plt.xlabel('날씨')
plt.ylabel('어린이 입장객수')
# plt.show()

# seaborn으로 막대 그래프 그리기
# sns.barplot(data=df, x='요일', y='청소년', errorbar=None)

# 그룹으로 묶어서 시각화 : hue 매개변수
sns.barplot(data=df, x='날씨', y='어린이', errorbar=None, hue='공휴일')

plt.show()