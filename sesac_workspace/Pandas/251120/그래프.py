import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("C:/sesac_worksapce/251120/seoul_park.csv")

#----------------------------------------------------------------------------------

# 박스플롯 그리기
# df_2016 = df[df["연"] == 2016]
# sns.boxplot(data = df_2016, x="월", y = '어른')
# plt.show()

#----------------------------------------------------------------------------------

# 산점도 그리기
# seaborn 사용
# sns.scatterplot(data = df, x='어른', y='어린이')
# 이상치로 인해 범위가 극단적으로 나올때 -> xlim, ylim으로 범위 제한
# plt.xlim(0,35000)
# plt.ylim(0,6000)

# # matplotlib 사용
# plt.scatter(df["어른"], df["청소년"])
# plt.show()

#----------------------------------------------------------------------------------

#히트맵 그리기(상관계수 데이터프레임 필요)
# df 데이터프레임에서 상관계수 구하기
df_corr = df.corr(numeric_only=True)
print(df_corr)
# annot=True : 실제 값도 히트맵에 출력
# fmt : 출력되는 값의 형식 지정(ex. 소숫점 자리)
# cmap : 출력되는 색상 맵의 테마 변경
sns.heatmap(df_corr, annot=False, cmap="viridis", fmt = ".2f")
plt.show()