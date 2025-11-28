import pandas as pd

df = pd.read_csv("251117/seoul_park04.csv")
df2 = pd.read_csv("251117/seoul_park_april.csv")

print(df.head())
print(df2.head())

#데이터 합치기
#df와 df2를 합치는데, 세로로 합칠 것이며, 겹치는 컬럼끼리 함칠것이고 합치고 난 뒤 인덱스 초기화
df_new = pd.concat([df, df2], axis = 0, join='inner', ignore_index=True)
print(df_new)
print(df_new.shape) #데이터 프레임 행,열 개수 반환(튜플 형태)
print(df_new.columns) #병합한 데이터 프레임 컬럼 출력