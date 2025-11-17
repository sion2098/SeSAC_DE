import pandas as pd

df = pd.read_csv("251117/seoul_park04.csv")

# print(df[df["어른"] > 2000]) #어른 컬럼을 series 형태로 추출한 다음 값이 1000보다 큰 값을 다시 추출
'''
df['어른' > 1000] (x)
df['어른'] > 1000 (x)
if df['어른'] > 1000 :  (x)
'''
#print(df[(df['어른'] > 1000) & (df['어린이'] > 1000)])

# print(df[df['날씨'].str.contains("맑음")])

#Q1. 어른이 10000 초과이고, 공휴일인 데이터 조회
# print(df[(df['어른'] > 10000) & (df['공휴일'] == 'O')])

#Q2. 어른이 10000 초과이거나, 어린이가 2000 초과인 데이터 조회
# print(df[(df['어른'] > 10000) | (df['어린이'] > 2000)])

#Q3. 5월 5일(어린이날) 데이터 조회
# df['날짜'] = pd.to_datetime(df['날짜'])
# df.info()
# print(df[(df['날짜'].dt.month == 5) & (df['날짜'].dt.day == 5)])
# print(df[(df['월'] == 5) & (df['일'] == 5)])

#print(df.loc[(df['어른'] > 1000) | (df['어린이'] > 1000), ['날짜','공휴일','어른','어린이']])

'''#print(df)
#Q1. 인덱스가 3이고, 컬럼이 어른인 데이터 조회
print(df.loc[3,'어른'])
#Q2. 인덱스가 3부터 6이고, 컬럼이 어른부터 외국인 조회
print(df.loc[3:6 ,'어른':'외국인'])
#Q3. 어른이 1000초과이고, 어린이가 1000 초과인 행에서 날짜부터 총계 조회
print(df.loc[(df['어른'] > 1000) & (df['어린이'] > 1000), "날짜":"단체"])'''


'''#print(df.head())
df_sorted = df.sort_values("총입장객수")
print(df_sorted.reset_index())
print(df_sorted.reset_index(drop=True))

print("="*30)
'''
'''df = df.drop(["날씨","요일"], axis=1)
df = df.drop(0, axis=0)
print(df)
'''
'''df.rename(columns= {"총입장객수" : "총계"}, inplace=True)
print(df)'''


print(df.isna().sum()) # 데이터프레임의 모든 컬럼에 대해 결측값의 개수 반환
#df['청소년'] = df['청소년'].fillna(int(df['청소년'].mean()))

#dropna() : 행삭제 -> 행 삭제 후 print(df.shape)하면 행 줄어든거 볼 수 있음
df.dropna(subset=['청소년'], ignore_index=True, inplace=True)
print(df.isna().sum())
print(df.shape)