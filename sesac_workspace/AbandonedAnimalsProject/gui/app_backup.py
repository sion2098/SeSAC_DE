# 이거 일단 실행 잘됨(초안)
# # =========================
# # 0. 라이브러리 불러오기
# # =========================
# import streamlit as st         # Streamlit GUI
# import pandas as pd            # 데이터프레임 처리
# import matplotlib.pyplot as plt
# import seaborn as sns

# # =========================
# # 1. CSV 불러오기 및 컬럼 추가
# # =========================
# @st.cache_data
# def load_data(csv_path):
#     """
#     CSV 파일을 불러온 후, 필요한 계산 컬럼 생성
#     - month: 발생 월
#     - weekday: 발생 요일
#     - age_months: 나이(개월) 계산
#     - weight: 체중(Kg) 변환
#     """
#     # CSV에는 원본 컬럼만 존재
#     cols = ["happenDt","upKindNm","kindNm","happenPlace","sexCd","age","weight"]
#     df = pd.read_csv(csv_path, usecols=cols)
    
#     # 날짜 컬럼 datetime 변환
#     df["happenDt"] = pd.to_datetime(df["happenDt"], format="%Y-%m-%d")
    
#     # 월과 요일 컬럼 추가
#     df["month"] = df["happenDt"].dt.month
#     df["weekday"] = df["happenDt"].dt.day_name()
    
#     # 나이를 개월수로 변환
#     def age_to_months(age_str):
#         if pd.isna(age_str):
#             return None
#         if "60일" in age_str:
#             return 0
#         year = ''.join(filter(str.isdigit, age_str.split("(")[0]))
#         if year.isdigit():
#             return (2025 - int(year)) * 12
#         return None
#     df["age_months"] = df["age"].apply(age_to_months)
    
#     # 체중 문자열 전처리
#     def convert_weight(w):
#         if pd.isna(w):
#             return None
#         w = w.replace("(Kg)", "").strip()
#         if "~" in w:
#             parts = w.split("~")
#             try:
#                 return (float(parts[0]) + float(parts[1])) / 2
#             except:
#                 return None
#         try:
#             return float(w)
#         except:
#             return None
#     df["weight"] = df["weight"].apply(convert_weight)
    
#     return df

# # CSV 파일 경로
# csv_path = "C:/Users/USER/Desktop/SeSAC_DE/sesac_workspace/AbandonedAnimalsProject/data/abandoned_animals_2025.csv"
# df = load_data(csv_path)  # 데이터 로드 및 컬럼 생성

# # =========================
# # 2. Streamlit 제목 및 설명
# # =========================
# st.title("유기동물 데이터 대시보드")
# st.markdown("유기동물 데이터 시각화 및 통계 분석 (탭 기반 Interactive Dashboard)")

# # =========================
# # 3. 탭 생성
# # =========================
# tab1, tab2, tab3 = st.tabs(["동물 종류 & 품종", "유기 장소 패턴", "유기 시기 분석"])

# # =========================
# # 3-1. 첫 번째 탭: 동물 종류 & 품종 분석
# # =========================
# with tab1:
#     st.header("유기 동물 종류 및 품종 분석")
    
#     # 동물 종류별 수
#     st.subheader("유기 동물 종류별 수")
#     st.bar_chart(df["upKindNm"].value_counts())
    
#     # 상위 품종별 수 (동물 종류별 상위 10)
#     st.subheader("상위 품종별 수 (동물 종류별 상위 10)")
#     top_breeds = df.groupby("upKindNm")["kindNm"].value_counts().groupby(level=0).head(10)
#     st.dataframe(top_breeds)

# # =========================
# # 3-2. 두 번째 탭: 유기 장소 패턴 분석
# # =========================
# with tab2:
#     st.header("유기 장소 패턴")
    
#     # 유기 장소별 수 상위 20
#     st.subheader("유기 장소별 수 (상위 20)")
#     top_places = df["happenPlace"].value_counts().head(20)
#     st.bar_chart(top_places)
    
#     # 지도 시각화 (좌표 없으면 bar chart 대체)
#     # 실제 좌표 정보가 있다면 st.map()으로 표시 가능

# # =========================
# # 3-3. 세 번째 탭: 유기 시기 분석
# # =========================
# with tab3:
#     st.header("유기 시기 분석")
    
#     # 필터: 날짜 선택
#     st.subheader("필터 설정: 날짜 범위")
#     start_date = st.date_input("시작 날짜", df["happenDt"].min())
#     end_date = st.date_input("종료 날짜", df["happenDt"].max())
    
#     filtered_df = df[(df["happenDt"] >= pd.to_datetime(start_date)) &
#                      (df["happenDt"] <= pd.to_datetime(end_date))]
    
#     st.markdown(f"### 필터 적용 후 데이터 수: {len(filtered_df)}")
#     st.dataframe(filtered_df.head(10))
    
#     # 월별 유기 동물 수
#     st.subheader("월별 유기 동물 수")
#     month_counts = filtered_df["month"].value_counts().sort_index()
#     st.bar_chart(month_counts)
    
#     # 요일별 유기 동물 수
#     st.subheader("요일별 유기 동물 수")
#     weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#     weekday_counts = filtered_df["weekday"].value_counts().reindex(weekday_order)
#     st.bar_chart(weekday_counts)
    
#     # 나이, 체중, 성별 분포
#     st.subheader("나이(개월) 분포")
#     fig1, ax1 = plt.subplots()
#     sns.histplot(filtered_df["age_months"].dropna(), bins=20, kde=True, ax=ax1)
#     st.pyplot(fig1)
    
#     st.subheader("체중(Kg) 분포")
#     fig2, ax2 = plt.subplots()
#     sns.histplot(filtered_df["weight"].dropna(), bins=20, kde=True, ax=ax2)
#     st.pyplot(fig2)
    
#     st.subheader("성별 분포")
#     st.bar_chart(filtered_df["sexCd"].value_counts())

# # =========================
# # 4. 데이터 다운로드 버튼
# # =========================
# st.header("데이터 다운로드")
# st.download_button(
#     label="필터 적용 데이터 다운로드 (CSV)",
#     data=filtered_df.to_csv(index=False, encoding="utf-8-sig"),
#     file_name="abandoned_animals_filtered.csv",
#     mime="text/csv"
# )