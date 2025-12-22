import pandas as pd

df = pd.read_csv("251117/seoul_park_april.csv")
print(df)

print(df.isna().sum())