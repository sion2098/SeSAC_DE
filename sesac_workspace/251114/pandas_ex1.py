import pandas as pd

df = pd.read_csv("251114/seoul_park.csv")

grouped = df.groupby("날씨")["총계"].mean()
print(grouped)