import streamlit as st
import pandas as pd

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("trails.csv")
    return df

df = load_data()

st.title("🏞️ 산책로 추천 시스템")
st.write("원하는 조건을 선택하면 맞춤 산책로를 추천해드릴게요!")

# -----------------------------
# 사용자 입력 UI
# -----------------------------
location = st.selectbox("지역을 선택하세요", ["전체"] + sorted(df["location"].unique()))
difficulty = st.selectbox("난이도 선택", ["전체", "easy", "normal", "hard"])
max_length = st.slider("최대 산책로 길이(km)", 1, 20, 10)
tag_input = st.text_input("원하는 키워드 (예: 호숫가, 숲길 등)")

# -----------------------------
# 산책로 필터링
# -----------------------------
filtered = df.copy()

if location != "전체":
    filtered = filtered[filtered["location"] == location]

if difficulty != "전체":
    filtered = filtered[filtered["difficulty"] == difficulty]

filtered = filtered[filtered["length_km"] <= max_length]

# 키워드 필터링
if tag_input.strip():
    keywords = [t.strip() for t in tag_input.split(",")]
    for kw in keywords:
        filtered = filtered[filtered["tags"].str.contains(kw, case=False, na=False)]

# -----------------------------
# 추천 점수 계산
# -----------------------------
if not filtered.empty:
    filtered["recommend_score"] = (
        (5 - filtered["crowded_score"]) * 0.4 +
        filtered["scenery_score"] * 0.6
    )
    filtered = filtered.sort_values(by="recommend_score", ascending=False)
else:
    st.error("조건에 맞는 산책로가 없습니다.")
    st.stop()

# -----------------------------
# 결과 출력
# -----------------------------
st.subheader("📌 추천 산책로 Top 5")
st.dataframe(filtered.head(5))

# 지도 표시 (선택)
if st.checkbox("📍 지도에서 보기 (샘플 좌표 있어야 작동)"):
    if {"lat", "lon"}.issubset(filtered.columns):
        st.map(filtered[["lat", "lon"]].head(50))
    else:
        st.warning("CSV에 lat, lon 컬럼이 있어야 지도 표시가 가능합니다.")
