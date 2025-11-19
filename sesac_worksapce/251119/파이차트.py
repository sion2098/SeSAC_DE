import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("251119/seoul_park.csv")
print(df)

# 파이차트 그리기
data_2019 = df[df['연'] == 2019][['어른','청소년','어린이']].sum()  #'연' 컬럼에서 데이터값이 2019인 값 추출 > '어른','어린이','청소년' 값 sum()해서 출력
# 출력한 형태 : Series 형태
print(data_2019)
print(type(data_2019))
# 인덱스를 가져와서 리스트 형태로 반환 ['어른','청소년','어린이']
labels = data_2019.index.tolist() 
data = data_2019.tolist()
#값을 가져와서 리스트 형태로 반환 [103125, 3817, 15209]
print(labels)
print(data)

# 파이차트 함수: pie()
plt.pie(x=data, labels = labels, autopct='%.1f%%')
#autopct: 각 범주의 실제 비율 값을 포맷 문자열 형식으로 출력
#%: 포맷 문자열의 시작을 알림
# .1f: 소수점 첫재짜리까지 반올림
# %%: 진짜 % 문자 그 자체(이스케이프 처리)
plt.legend(loc = 'lower left') #loc : 범례의 위치 조절
plt.show()