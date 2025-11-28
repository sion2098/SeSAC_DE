import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("251119/seoul_park.csv")

#데이터 가공 : '요일' 컬럼의 값이 '토'인 데이터 추출
df_sat = df[df['요일'] == '토']
#print(df_sat)

# matplotlib으로 '어린이' 컬럼의 각 구간 빈도
# plt.hist(df_sat['어린이'], bins=35)  #bins : 구간의 개수(=막대의 개수) 설정


#seaborn으로 '어른' 컬럼의 각 구간 빈도
#sns.histplot(data=df_sat, x='어른')


# #그룹화 ; 2월 데이터만 뽑아 어린이의 빈도수를 구하는데 연도별로 그룹화 함
# df_feb = df[df['월'] == 2]
# sns.histplot(data=df_feb, 
#              x='어린이', 
#              hue='연', 
#              binrange=(0,1000), 
#              bins=10, 
#              multiple='dodge', #여러 그래프의 막대끼리 겹치지 않게
#              shrink=0.8) #기존의 80%의 막대 너비로 설정
# plt.show()


## 미니 실습
## 2017년 4월의 어른 이용객의 히스토그램을 그리세요
## 구간은 20개로 나눕니다
# df_2017 = df[df['연'] == 2017]  # 한줄 작성 ver : df_2017_april = df[(df['연'] == 2017) & (df['월'] == 4)]
# df_april = df_2017[df_2017['월'] == 4]
# print(df_april)
# sns.histplot(data=df_april, 
#              x ='어른', 
#              bins = 20
#              )
# plt.show()


sns.countplot(data=df, x='날씨', hue = '공휴일')
plt.show()