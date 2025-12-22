import pandas as pd

df = pd.read_csv("251117/seoul_park_april.csv")

print(df.sort_values("총계"))