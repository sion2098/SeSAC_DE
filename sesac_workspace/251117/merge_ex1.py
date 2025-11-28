import pandas as pd

df = pd.read_csv("251117/seoul_park04.csv")
df2 = pd.read_csv("251117/seoul_park_april.csv")
mm = pd.read_csv("251117/misemunji.csv")

print(df.head())
print(mm.head())

#날짜 기준으로 df와 mm 데이터셋 병합
# 입장객 뎅이터의 일부 날짜가 날라가지 않게 left를 기준으로 merge
merged_df = pd.merge(df, mm, on='날짜',how='left')
print(merged_df)
print(mm.isna().sum())
