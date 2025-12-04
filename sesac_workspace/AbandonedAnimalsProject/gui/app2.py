# =========================
# 0. 라이브러리 불러오기
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
import altair as alt
import re

# 페이지 전체 폭 확장
st.set_page_config(layout="wide")

# 한글 깨짐 방지
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =========================
# 1. CSV 불러오기 및 전처리
# =========================
@st.cache_data
def load_data(csv_path):
    """
    CSV 불러오기 + 날짜/월/요일/나이/체중/장소 카테고리 컬럼 추가
    """
    cols = ["happenDt","upKindNm","kindNm","happenPlace","sexCd","age","weight","province"]
    df = pd.read_csv(csv_path, usecols=cols)

    # 날짜 처리
    df["happenDt"] = pd.to_datetime(df["happenDt"], format="%Y-%m-%d")
    df["month"] = df["happenDt"].dt.month
    df["weekday"] = df["happenDt"].dt.day_name()

    # 나이 → 개월수 변환
    def age_to_months(age_str):
        if pd.isna(age_str):
            return None
        if "60일" in age_str:  # 2개월 이하
            return 0
        year = ''.join(filter(str.isdigit, age_str.split("(")[0]))
        return (2025 - int(year)) * 12 if year.isdigit() else None
    df["age_months"] = df["age"].apply(age_to_months)

    # 체중 전처리
    def convert_weight(w):
        if pd.isna(w):
            return None
        w = w.replace("(Kg)", "").strip()
        if "~" in w:
            try:
                parts = w.split("~")
                return (float(parts[0]) + float(parts[1])) / 2
            except: 
                return None
        try:
            return float(w)
        except:
            return None
    df["weight"] = df["weight"].apply(convert_weight)

    # 장소 분류
    def categorize_place(place):
        if pd.isna(place):
            return "기타"
        text = re.sub(r"\s+","", str(place)).lower()
        patterns = [
            ("주거지역", r"(아파트|주택|빌라|단지|주공|연립|후문|세대)"),
            ("공원/산책로", r"(공원|산책|둘레길|산책로|공원로)"),
            ("산/야산", r"(야산|능선|봉$|봉\W|산\d|(^|[^\w])산([^\w]|$))"),
            ("하천/해안", r"(천|강|하천|강변|해변|바닷가|호수|둔치)"),
            ("공공시설", r"(역\b|터미널|정류장|버스정류장|기차역|지하철역)"),
            ("학교/교육시설", r"(학교|초등학교|중학교|고등학교|대학|캠퍼스|학원)"),
            ("상업지역", r"(시장|마트|아울렛|상가|편의점|주유소|백화점|몰|식당|카페)"),
            ("산업단지", r"(산단|산업단지|공장|공업단지|공단)"),
            ("도로/거리", r"(로\b|길\b|대로\b|번길\b|번지\b|도로\b|국도|지방도)"),
            ("마을", r"(리\b|마을|읍\b|면\b|동\b)")
        ]
        for cat, pat in patterns:
            if re.search(pat, text):
                return cat
        return "기타"
    df["place_category"] = df["happenPlace"].apply(categorize_place)

    return df

# 데이터 불러오기
csv_path = "C:/Users/USER/Desktop/SeSAC_DE/sesac_workspace/AbandonedAnimalsProject/data/abandoned_animals_2025.csv"
df = load_data(csv_path)

# =========================
# 2. Streamlit 기본 설정
# =========================
st.title("유기동물 데이터 대시보드")

# =========================
# 3. 탭 생성
# =========================
tab1, tab2, tab3 = st.tabs(["장소 패턴", "시기 분석", "동물 종류 & 품종"])

# =========================
# 3-1. 동물 종류 & 품종 분석
# =========================
with tab3:
    st.header("유기 동물 종류 및 품종 분석")

    col1, col2 = st.columns([1.5, 1])

    # ▪️ 좌측: 종류별 수
    with col1:
        df["kind_group"] = df["upKindNm"].map({"개":"강아지", "고양이":"고양이"}).fillna("기타")
        kind_counts = df["kind_group"].value_counts().reset_index()
        kind_counts.columns = ["kind_group","count"]

        base = alt.Chart(kind_counts).encode(
            x=alt.X("kind_group:N", axis=alt.Axis(labelAngle=0)),
            y="count:Q"
        )
        chart = (base.mark_bar() + base.mark_text(align="center", baseline="bottom", dy=-2, fontSize=14, text="count:Q")).properties(height=350)
        st.altair_chart(chart, use_container_width=True)

    # ▪️ 우측: 품종 Top3
    with col2:
        card_style = """
        <style>
        .animal-card { background:#fff; border-radius:15px; padding:18px; margin-bottom:18px; box-shadow:0 4px 10px rgba(0,0,0,0.1); border-left:7px solid #6C63FF; }
        .animal-title { font-size:20px; font-weight:bold; margin-bottom:10px; }
        .breed-item { font-size:15px; padding:4px 0; }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)

        def render_top3(kind_name, emoji):
            top3 = df[df["upKindNm"]==kind_name]["kindNm"].value_counts().head(3)
            html = f"<div class='animal-card'><div class='animal-title'>{emoji} {kind_name} TOP 3</div>"
            for i, (breed, count) in enumerate(top3.items(), 1):
                html += f"<div class='breed-item'>{i}. {breed} — {count}건</div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        render_top3("개", "🐶")
        render_top3("고양이", "🐱")

# =========================
# 3-2. 장소 패턴 분석
# =========================
with tab1:
    st.header("지역별 유기동물 분포 지도")
    province_counts = df['province'].value_counts().reset_index()
    province_counts.columns = ['province','count']
    province_counts['percent'] = province_counts['count']/len(df)*100

    species_counts = df.pivot_table(index='province', columns='upKindNm', aggfunc='size', fill_value=0)
    province_counts = province_counts.merge(species_counts, on='province', how='left').fillna(0)

    map_col, list_col = st.columns([2.2,1])

    # ▪️ 지도
    with map_col:
        m = folium.Map(location=[36.5,127.5], zoom_start=7)
        province_coords = { "서울특별시":[37.5665,126.9780], "부산광역시":[35.1796,129.0756], "대구광역시":[35.8714,128.6014], "인천광역시":[37.4563,126.7052], 
                            "광주광역시":[35.1595,126.8526], "대전광역시":[36.3504,127.3845], "울산광역시":[35.5396,129.3114], "세종특별자치시":[36.4800,127.2890],
                            "경기도":[37.4138,127.5183], "강원특별자치도":[37.8228,128.1555], "충청북도":[36.6357,127.4910], "충청남도":[36.5184,126.8000],
                            "전북특별자치도":[35.8200,127.1080], "전라남도":[34.8161,126.4620], "경상북도":[36.4919,128.8889], "경상남도":[35.3450,128.4380],
                            "제주특별자치도":[33.5000,126.5312] }

        for _, row in province_counts.iterrows():
            prov = row['province']
            if prov not in province_coords: continue
            popup_html = f"""
            <div style="font-family:Malgun Gothic">
                <b style="font-size:14px">{prov}</b><br>
                총 유기동물 수: {row['count']} ({row['percent']:.1f}%)<br>
                강아지: {row.get('개',0)}건<br>
                고양이: {row.get('고양이',0)}건<br>
                기타: {row.get('기타',0)}건
            </div>
            """
            folium.CircleMarker(
                location=province_coords[prov],
                radius=max(10,10+row['count']/500),
                color="blue", fill=True, fill_color="skyblue", fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(m)
        st_folium(m, width=750, height=700)

# =========================
# 3-3. 유기 시기 분석
# =========================
with tab2:
    st.header("📅 유기 시기 분석 대시보드")

    # ▪️ 기간 필터
    start_date = st.date_input("시작 날짜", df["happenDt"].min())
    end_date = st.date_input("종료 날짜", df["happenDt"].max())
    filtered_df = df[(df["happenDt"]>=start_date) & (df["happenDt"]<=end_date)]
    filtered_df = filtered_df[filtered_df['upKindNm'].isin(['개','고양이'])].sort_values('happenDt')

    # ▪️ KPI 카드 함수
    def render_kpi(col, title_dog, value_dog, title_cat, value_cat):
        html = f"""
        <div class="kpi-card kpi-dog"><div class="kpi-title">{title_dog}</div><div class="kpi-value">{value_dog}</div></div>
        <div class="kpi-card kpi-cat"><div class="kpi-title">{title_cat}</div><div class="kpi-value">{value_cat}</div></div>
        """
        col.markdown(html, unsafe_allow_html=True)

    # KPI 계산
    total_dog = len(filtered_df[filtered_df['upKindNm']=='개'])
    total_cat = len(filtered_df[filtered_df['upKindNm']=='고양이'])
    dog_top_month = filtered_df[filtered_df['upKindNm']=='개']['month'].value_counts().idxmax() if total_dog>0 else None
    cat_top_month = filtered_df[filtered_df['upKindNm']=='고양이']['month'].value_counts().idxmax() if total_cat>0 else None
    dog_top_season = filtered_df[filtered_df['upKindNm']=='개']['month'].apply(lambda m: ['겨울','봄','여름','가을'][ (m%12)//3 ] ).mode()[0] if total_dog>0 else None
    cat_top_season = filtered_df[filtered_df['upKindNm']=='고양이']['month'].apply(lambda m: ['겨울','봄','여름','가을'][(m%12)//3]).mode()[0] if total_cat>0 else None
    filtered_df['age_group'] = filtered_df.apply(lambda r: ('아기견' if r['age_months']<12 else '성견') if r['upKindNm']=='개' else ('아기묘' if r['age_months']<12 else '성묘'), axis=1)
    dog_age_top = filtered_df[filtered_df['upKindNm']=='개']['age_group'].value_counts().idxmax() if total_dog>0 else None
    cat_age_top = filtered_df[filtered_df['upKindNm']=='고양이']['age_group'].value_counts().idxmax() if total_cat>0 else None
    dog_sex_str = f"M:{filtered_df[filtered_df['upKindNm']=='개']['sexCd'].value_counts().get('M',0)} / F:{filtered_df[filtered_df['upKindNm']=='개']['sexCd'].value_counts().get('F',0)}"
    cat_sex_str = f"M:{filtered_df[filtered_df['upKindNm']=='고양이']['sexCd'].value_counts().get('M',0)} / F:{filtered_df[filtered_df['upKindNm']=='고양이']['sexCd'].value_counts().get('F',0)}"

    kpi_cols = st.columns(5)
    render_kpi(kpi_cols[0], "총 유기동물 (강아지)", total_dog, "총 유기동물 (고양이)", total_cat)
    render_kpi(kpi_cols[1], "최다 발생 월 (강아지)", f"{dog_top_month}월", "최다 발생 월 (고양이)", f"{cat_top_month}월")
    render_kpi(kpi_cols[2], "최다 발생 계절 (강아지)", dog_top_season, "최다 발생 계절 (고양이)", cat_top_season)
    render_kpi(kpi_cols[3], "주로 유기되는 나이대 (강아지)", dog_age_top, "주로 유기되는 나이대 (고양이)", cat_age_top)
    render_kpi(kpi_cols[4], "성별 분포 (강아지)", dog_sex_str, "성별 분포 (고양이)", cat_sex_str)

    # ▪️ 인사이트
    insight_html = "<div class='insight-box'><b>종합결론:</b><br>"
    if dog_age_top: insight_html += f"🐶 강아지: 주로 {dog_age_top}이 많이 유기되고 있습니다.<br>"
    if cat_age_top: insight_html += f"🐱 고양이: 주로 {cat_age_top}이 많이 유기되고 있습니다.<br>"
    insight_html += "</div>"
    st.markdown(insight_html, unsafe_allow_html=True)
