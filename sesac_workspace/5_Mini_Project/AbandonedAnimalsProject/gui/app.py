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
# 1. CSV 불러오기 및 컬럼 추가
# =========================
@st.cache_data
def load_data(csv_path):
    """
    CSV 파일 불러오기 및 계산 컬럼 추가
    - month: 발생 월
    - weekday: 발생 요일
    - age_months: 나이(개월)
    - weight: 체중(Kg)
    - province: 시/도 추출
    """
    cols = ["happenDt","upKindNm","kindNm","happenPlace","sexCd","age","weight","province"]
    df = pd.read_csv(csv_path, usecols=cols)
    
    # 날짜 컬럼 datetime 변환
    df["happenDt"] = pd.to_datetime(df["happenDt"], format="%Y-%m-%d")
    
    # 월과 요일 컬럼 추가
    df["month"] = df["happenDt"].dt.month
    df["weekday"] = df["happenDt"].dt.day_name()
    
    # 나이를 개월수로 변환
    def age_to_months(age_str):
        if pd.isna(age_str):
            return None
        if "60일" in age_str:
            return 0
        year = ''.join(filter(str.isdigit, age_str.split("(")[0]))
        if year.isdigit():
            return (2025 - int(year)) * 12
        return None
    df["age_months"] = df["age"].apply(age_to_months)
    
    # 체중 전처리
    def convert_weight(w):
        if pd.isna(w):
            return None
        w = w.replace("(Kg)", "").strip()
        if "~" in w:
            parts = w.split("~")
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return None
        try:
            return float(w)
        except:
            return None
    df["weight"] = df["weight"].apply(convert_weight)
    
    # # province 컬럼 생성 (happenPlace 전체 -> 시/도만 추출)
    # def extract_province(place):
    #     if pd.isna(place):
    #         return None
    #     return place.split()[0]
    # df["happenPlace"] = df["happenPlace"].apply(extract_province)

# =========================
    # 🔴 NEW: happenPlace 기반 장소 분류 함수 (10개 카테고리)
    # - 결과는 df["place_category"] 컬럼에 저장
    # 카테고리: 주거지역, 도로/거리, 상업지역, 공원/산책로, 산/야산,
    #           하천/해안, 공공시설, 학교/교육시설, 산업단지, 기타
    # =========================
    def categorize_place(place):
        # 안전 처리
        if pd.isna(place):
            return "기타"
        # 원문을 보존한 채로 비교하기 위해 원본(공백 유지)과 축약(text_no_space) 둘 다 사용
        place_str = str(place)
        text = re.sub(r"\s+", "", place_str)  # 공백 제거한 버전
        text_low = text.lower()  # 영문이 포함될 가능성 대비 소문자화
        
        # 우선순위 규칙 적용 (중요한 키워드를 먼저 체크)
        # 1) 주거지역
        if re.search(r"(아파트|주택|빌라|단지|주공|연립|후문|세대)", text_low):
            return "주거지역"
        # 2) 공원/산책로
        if re.search(r"(공원|산책|둘레길|산책로|공원로)", text_low):
            return "공원/산책로"
        # 3) 산/야산(지형)
        # 산 + 숫자(산37-27) 또는 '야산' 등
        if re.search(r"(야산|능선|봉$|봉\W|산\d|(^|[^\w])산([^\w]|$))", text_low):
            return "산/야산"
        # 4) 하천/강/해안
        if re.search(r"(천|강|하천|강변|해변|바닷가|호수|둔치)", text_low):
            return "하천/해안"
        # 5) 교통시설(역/터미널/정류장)
        if re.search(r"(역\b|터미널|정류장|버스정류장|기차역|지하철역)", place_str):
            return "공공시설"  # 교통시설을 공공시설로 합침 (하단에서 학교/기타로 분류 가능)
        # 6) 학교/교육시설
        if re.search(r"(학교|초등학교|중학교|고등학교|대학|캠퍼스|학원)", place_str):
            return "학교/교육시설"
        # 7) 상업지역 (시장/마트/아울렛/상가/주유소 등)
        if re.search(r"(시장|마트|아울렛|상가|편의점|주유소|백화점|몰|식당|카페)", text_low):
            return "상업지역"
        # 8) 산업단지/공장
        if re.search(r"(산단|산업단지|공장|공업단지|공단)", text_low):
            return "산업단지"
        # 9) 도로/거리 (로, 길, 대로, 번길, 번지 등)
        if re.search(r"(로\b|길\b|대로\b|번길\b|번지\b|도로\b|국도|지방도)", place_str):
            return "도로/거리"
        # 10) 마을/리 (읍/면/리/마을 등)
        if re.search(r"(리\b|마을|읍\b|면\b|동\b)", place_str):
            # '동'은 주거지역으로 중복될 수 있으므로 주거지역 키워드가 없을 때만 마을로 분류
            if re.search(r"(아파트|주택|빌라|단지)", text_low):
                return "주거지역"
            return "마을"
        # 기본: 기타
        return "기타"
    
    # 🔴 컬럼 생성
    df["place_category"] = df["happenPlace"].apply(categorize_place)
    # =========================
    # 🔴 장소 분류 컬럼 완성
    # =========================    

    
    return df

# CSV 파일 경로
csv_path = "C:/Users/USER/Desktop/SeSAC_DE/sesac_workspace/AbandonedAnimalsProject/data/abandoned_animals_2025.csv"
df = load_data(csv_path)

# =========================
# 2. Streamlit 제목 및 설명
# =========================
st.title("유기동물 데이터 대시보드")
# st.markdown("탭 기반 Interactive Dashboard: 종류/품종, 장소, 시기 분석")

# =========================
# 3. 탭 생성
# =========================
tab1, tab2, tab3 = st.tabs(["장소 패턴", "시기 분석", "동물 종류 & 품종"])

# =========================
# 탭3: 유기 동물 종류 & 품종 분석
# =========================
with tab3:
    # st.header("유기 동물 종류 및 품종 분석")

    # -------------------------
    # 1행: 동물 종류별 수 그래프
    # -------------------------
    col_graph = st.columns(1)[0]  # 한 열
    col_graph.subheader("유기 동물 종류별 수")

    # upKindNm -> kind_group 변환
    def kind_group(kind):
        if kind == "개":
            return "강아지"
        elif kind == "고양이":
            return "고양이"
        else:
            return "기타"
    df["kind_group"] = df["upKindNm"].apply(kind_group)

    # 그룹별 수 집계
    kind_counts = df["kind_group"].value_counts().reset_index()
    kind_counts.columns = ["kind_group", "count"]

    # Altair 차트
    import altair as alt
    base = alt.Chart(kind_counts).encode(
        x=alt.X("kind_group:N", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("count:Q")
    )
    # 막대 폭 30으로 살짝 늘려서 가독성 확보
    bar = base.mark_bar(size=150)
    text = base.mark_text(
        align="center",
        baseline="bottom",
        dy=-2,
        fontSize=14
    ).encode(text="count:Q")
    chart = (bar + text).properties(height=280)
    col_graph.altair_chart(chart, use_container_width=True)

    # -------------------------
    # 2행: 강아지/고양이 Top5 품종
    # -------------------------
    col_dog, col_cat = st.columns(2)

    # CSS 카드 스타일
    card_style = """
    <style>
    .animal-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 18px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 7px solid #6C63FF;
    }
    .animal-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .breed-item {
        font-size: 15px;
        padding: 4px 0;
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    # -------------------------
    # 강아지 Top5
    # -------------------------
    col_dog.subheader("강아지 Top 5 품종")
    dog_top5 = df[df["upKindNm"] == "개"]["kindNm"].value_counts().head(5)
    dog_html = "<div class='animal-card'><div class='animal-title'>🐶 강아지 Top 5</div>"
    for idx, (breed, count) in enumerate(dog_top5.items(), start=1):
        dog_html += f"<div class='breed-item'>{idx}. {breed} — {count}건</div>"
    dog_html += "</div>"
    col_dog.markdown(dog_html, unsafe_allow_html=True)

    # -------------------------
    # 고양이 Top5
    # -------------------------
    col_cat.subheader("고양이 Top 5 품종")
    cat_top5 = df[df["upKindNm"] == "고양이"]["kindNm"].value_counts().head(5)
    cat_html = "<div class='animal-card'><div class='animal-title'>🐱 고양이 Top 5</div>"
    for idx, (breed, count) in enumerate(cat_top5.items(), start=1):
        cat_html += f"<div class='breed-item'>{idx}. {breed} — {count}건</div>"
    cat_html += "</div>"
    col_cat.markdown(cat_html, unsafe_allow_html=True)



# =========================
# 3-2. 두 번째 탭: 유기 장소 패턴 분석 (지방 전체 + 지역 선택 기능)
# =========================
with tab1:
    st.header("지역별 유기동물 분포 지도")

    # -----------------------------------------
    # 1. 기본 집계
    # -----------------------------------------
    province_counts = df['province'].value_counts().reset_index()
    province_counts.columns = ['province', 'count']
    total_animals = len(df)
    province_counts['percent'] = province_counts['count'] / total_animals * 100

    # -----------------------------------------
    # 2. 종별 pivot (개/고양이/기타)
    # -----------------------------------------
    species_counts = df.pivot_table(
        index='province',
        columns='upKindNm',
        aggfunc='size',
        fill_value=0
    )

    # -----------------------------------------
    # 3. 병합
    # -----------------------------------------
    province_counts = province_counts.merge(species_counts, on='province', how='left').fillna(0)
    for col in ['count'] + list(species_counts.columns):
        province_counts[col] = province_counts[col].astype(int)

    # -----------------------------------------
    # 🔵 MODIFIED: 레이아웃 비율 조정 (왼쪽 지도, 오른쪽 랭킹)
    # -----------------------------------------
    map_col, list_col = st.columns([2.2, 1])   # ⭐ 반영됨

    # =====================================================
    # LEFT AREA : 지도
    # =====================================================
    with map_col:

        # 정렬
        province_counts = province_counts.sort_values(by='province').reset_index(drop=True)

        # 지도 생성
        m = folium.Map(location=[36.5, 127.5], zoom_start=7)

        # 각 시/도 중심 좌표
        province_coords = {
            "서울특별시": [37.5665, 126.9780],
            "부산광역시": [35.1796, 129.0756],
            "대구광역시": [35.8714, 128.6014],
            "인천광역시": [37.4563, 126.7052],
            "광주광역시": [35.1595, 126.8526],
            "대전광역시": [36.3504, 127.3845],
            "울산광역시": [35.5396, 129.3114],
            "세종특별자치시": [36.4800, 127.2890],
            "경기도": [37.4138, 127.5183],
            "강원특별자치도": [37.8228, 128.1555],
            "충청북도": [36.6357, 127.4910],
            "충청남도": [36.5184, 126.8000],
            "전북특별자치도": [35.8200, 127.1080],
            "전라남도": [34.8161, 126.4620],
            "경상북도": [36.4919, 128.8889],
            "경상남도": [35.3450, 128.4380],
            "제주특별자치도": [33.5000, 126.5312]
        }

        # -----------------------------------------
        # 마커 생성 + 팝업(시/도명, 총 건수, 강아지/고양이/기타)
        # -----------------------------------------
        for idx, row in province_counts.iterrows():
            prov = row['province']
            if prov not in province_coords:
                continue

            popup_html = f"""
            <div style="font-family:Malgun Gothic">
                <b style="font-size:14px">{prov}</b><br>
                총 유기동물 수: {row['count']} ({row['percent']:.1f}%)<br>
                강아지: {row.get('개', 0)}건<br>
                고양이: {row.get('고양이', 0)}건<br>
                기타: {row.get('기타', 0)}건
            </div>
            """

            radius = max(10, 10 + row['count'] / 500)

            folium.CircleMarker(
                location=province_coords[prov],
                radius=radius,
                color="blue",
                fill=True,
                fill_color="skyblue",
                fill_opacity=0.6,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(m)

        # -----------------------------------------
        # 🔵 MODIFIED: 지도 height 증가 (700)
        # -----------------------------------------
        st_map = st_folium(m, width=750, height=700)

    # =====================================================
    # RIGHT AREA : 유기 장소 유형 TOP 5
    # =====================================================
    with list_col:
        st.subheader("유기 장소 유형 Top 5")

        # -------------------------
        # 지도 클릭 여부 확인
        # -------------------------
        clicked_province = None

        if st_map and st_map.get("last_object_clicked"):
            clicked_lat = st_map["last_object_clicked"].get("lat")
            clicked_lng = st_map["last_object_clicked"].get("lng")

            # 좌표 기반 province 추정
            for prov, coord in province_coords.items():
                if abs(coord[0] - clicked_lat) < 0.5 and abs(coord[1] - clicked_lng) < 0.5:
                    clicked_province = prov
                    break

        # -------------------------
        # 지역 필터
        # -------------------------
        if clicked_province:
            st.markdown(f"### 📍 선택한 지역: **{clicked_province}** 기준")
            filtered_df = df[df["province"] == clicked_province]
        else:
            st.markdown("### 전체 지역 기준")
            filtered_df = df

        # -------------------------
        # Top5 카테고리 집계
        # -------------------------
        cat_counts = (
            filtered_df["place_category"]
            .value_counts()
            .reset_index()
        )
        cat_counts.columns = ["category", "count"]

        # -------------------------
        # 카드 스타일
        # -------------------------
        card_css = """
        <style>
        .place-card {
            background: #ffffff;
            padding: 12px 14px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
            border-left: 6px solid #00a2ff;
        }
        .place-title { font-size:16px; font-weight:700; }
        .place-sub { color:#555; font-size:13px; margin-top:6px; }
        </style>
        """
        st.markdown(card_css, unsafe_allow_html=True)

        # -------------------------
        # Top5 리스트 표시
        # -------------------------
        for idx, row in cat_counts.head(5).iterrows():
            st.markdown(
                f"""
                <div class='place-card'>
                    <div class='place-title'>{idx+1}. {row['category']}</div>
                    <div class='place-sub'>유기 건수: {int(row['count'])}건</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------
        # 🔴 MODIFIED: 대표 샘플 주소 제거됨
        # -------------------------

        # -------------------------
        # 🔵 MODIFIED: 지도와 오른쪽 하단 높이 맞추기 위한 여백
        # -------------------------
        st.write("")
        st.write("")
        st.write("")


            
# =========================
# 3-3. 탭2: 유기 시기 분석 (월/계절 + KPI + 종합결론)
# =========================
with tab2:
    st.header("📅 유기 시기 분석 대시보드")

    # ===============================
    # 0) CSS: KPI 카드 + 인사이트 + 여백
    # ===============================
    st.markdown("""
        <style>
            /* KPI 카드 */
            .kpi-card {
                padding: 16px;
                border-radius: 12px;
                background: #ffffff;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                font-family: Malgun Gothic;
                color: #333;
                margin-bottom: 15px;
            }
            .kpi-title {
                font-size:13px; 
                color:#555;
            }
            .kpi-value {
                font-size:20px; 
                font-weight:700; 
                margin-top:6px;
            }
            /* 좌측 테두리 색상 */
            .kpi-dog { border-left: 6px solid #4e8cff; }
            .kpi-cat { border-left: 6px solid #2ecc71; }

            /* 종합결론 영역 */
            .insight-box {
                padding: 16px;
                border-radius: 12px;
                background: #f8f9fa;
                box-shadow: 0 3px 8px rgba(0,0,0,0.05);
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ===============================
    # 1) 1행: 기간 필터 + 그래프 2개 (3열)
    # ===============================
    col1, col2, col3 = st.columns([1,1,1])

    # --- 기간 필터 ---
    with col1:
        st.subheader("🔧 기간 설정")
        start_date = st.date_input("시작 날짜", df["happenDt"].min())
        end_date = st.date_input("종료 날짜", df["happenDt"].max())

    # 필터 적용
    filtered_df = df[(df["happenDt"] >= pd.to_datetime(start_date)) & 
                     (df["happenDt"] <= pd.to_datetime(end_date))].copy()
    filtered_df = filtered_df[filtered_df['upKindNm'].isin(['개','고양이'])]
    filtered_df = filtered_df.sort_values(by="happenDt", ascending=True)

    # --- 월별 그래프 ---
    with col2:
        monthly_counts = filtered_df.groupby(['month','upKindNm']).size().reset_index(name='count')
        fig1, ax1 = plt.subplots(figsize=(5,3))
        sns.barplot(data=monthly_counts, x='month', y='count', hue='upKindNm',
                    palette={'개':'skyblue','고양이':'lightgreen'}, ax=ax1)
        ax1.set_title("월별 유기동물 발생 건수", fontsize=12)
        st.pyplot(fig1)

    # --- 계절별 그래프 ---
    with col3:
        def get_season(m):
            if m in [3,4,5]: return '봄'
            elif m in [6,7,8]: return '여름'
            elif m in [9,10,11]: return '가을'
            else: return '겨울'
        filtered_df['season'] = filtered_df['happenDt'].dt.month.apply(get_season)
        season_order = ["봄","여름","가을","겨울"]
        season_counts = filtered_df.groupby(['season','upKindNm']).size().reset_index(name='count')
        season_counts['season'] = pd.Categorical(season_counts['season'], categories=season_order, ordered=True)
        season_counts = season_counts.sort_values('season')

        fig2, ax2 = plt.subplots(figsize=(5,3))
        sns.barplot(data=season_counts, x='season', y='count', hue='upKindNm',
                    palette={'개':'skyblue','고양이':'lightgreen'}, ax=ax2)
        ax2.set_title("계절별 유기동물 발생 건수", fontsize=12)
        st.pyplot(fig2)

    # ===============================
    # 2) 2행: KPI 카드 5개 (강아지/고양이 색상 구분)
    # ===============================
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    # KPI1: 총 유기동물 수
    total_dog = len(filtered_df[filtered_df['upKindNm']=='개'])
    total_cat = len(filtered_df[filtered_df['upKindNm']=='고양이'])
    kpi_html = f"""
        <div class="kpi-card kpi-dog">
            <div class="kpi-title">총 유기동물 (강아지)</div>
            <div class="kpi-value">{total_dog:,} 건</div>
        </div>
        <div class="kpi-card kpi-cat">
            <div class="kpi-title">총 유기동물 (고양이)</div>
            <div class="kpi-value">{total_cat:,} 건</div>
        </div>
    """
    kpi_col1.markdown(kpi_html, unsafe_allow_html=True)

    # KPI2: 최다 발생 월
    dog_top_month = filtered_df[filtered_df['upKindNm']=='개']['month'].value_counts().idxmax() if total_dog>0 else None
    cat_top_month = filtered_df[filtered_df['upKindNm']=='고양이']['month'].value_counts().idxmax() if total_cat>0 else None
    kpi_html = f"""
        <div class="kpi-card kpi-dog">
            <div class="kpi-title">최다 발생 월 (강아지)</div>
            <div class="kpi-value">{dog_top_month}월</div>
        </div>
        <div class="kpi-card kpi-cat">
            <div class="kpi-title">최다 발생 월 (고양이)</div>
            <div class="kpi-value">{cat_top_month}월</div>
        </div>
    """
    kpi_col2.markdown(kpi_html, unsafe_allow_html=True)

    # KPI3: 최다 발생 계절
    dog_top_season = filtered_df[filtered_df['upKindNm']=='개']['season'].value_counts().idxmax() if total_dog>0 else None
    cat_top_season = filtered_df[filtered_df['upKindNm']=='고양이']['season'].value_counts().idxmax() if total_cat>0 else None
    kpi_html = f"""
        <div class="kpi-card kpi-dog">
            <div class="kpi-title">최다 발생 계절 (강아지)</div>
            <div class="kpi-value">{dog_top_season}</div>
        </div>
        <div class="kpi-card kpi-cat">
            <div class="kpi-title">최다 발생 계절 (고양이)</div>
            <div class="kpi-value">{cat_top_season}</div>
        </div>
    """
    kpi_col3.markdown(kpi_html, unsafe_allow_html=True)

    # KPI4: 주로 유기되는 나이대
    # '아기견/아기묘', '성견/성묘' 기준
    def age_group(row):
        age = row['age_months']
        if pd.isna(age):
            return None
        if row['upKindNm']=='개':
            return '아기견' if age<12 else '성견'
        else:
            return '아기묘' if age<12 else '성묘'
    filtered_df['age_group'] = filtered_df.apply(age_group, axis=1)

    dog_age_top = filtered_df[filtered_df['upKindNm']=='개']['age_group'].value_counts().idxmax() if total_dog>0 else None
    cat_age_top = filtered_df[filtered_df['upKindNm']=='고양이']['age_group'].value_counts().idxmax() if total_cat>0 else None

    kpi_html = f"""
        <div class="kpi-card kpi-dog">
            <div class="kpi-title">주로 유기되는 나이대 (강아지)</div>
            <div class="kpi-value">{dog_age_top}</div>
        </div>
        <div class="kpi-card kpi-cat">
            <div class="kpi-title">주로 유기되는 나이대 (고양이)</div>
            <div class="kpi-value">{cat_age_top}</div>
        </div>
    """
    kpi_col4.markdown(kpi_html, unsafe_allow_html=True)

    # KPI5: 성별 분포 (M/F)
    dog_sex = filtered_df[filtered_df['upKindNm']=='개']['sexCd'].value_counts()
    cat_sex = filtered_df[filtered_df['upKindNm']=='고양이']['sexCd'].value_counts()
    dog_sex_str = f"M:{dog_sex.get('M',0)} / F:{dog_sex.get('F',0)}"
    cat_sex_str = f"M:{cat_sex.get('M',0)} / F:{cat_sex.get('F',0)}"
    kpi_html = f"""
        <div class="kpi-card kpi-dog">
            <div class="kpi-title">성별 분포 (강아지)</div>
            <div class="kpi-value">{dog_sex_str}</div>
        </div>
        <div class="kpi-card kpi-cat">
            <div class="kpi-title">성별 분포 (고양이)</div>
            <div class="kpi-value">{cat_sex_str}</div>
        </div>
    """
    kpi_col5.markdown(kpi_html, unsafe_allow_html=True)

    # ===============================
    # 3) 3행: 종합결론 인사이트
    # ===============================
    insight_html = "<div class='insight-box'><b>종합결론:</b><br>"

    if total_dog>0:
        insight_html += f"🐶 강아지: 주로 {dog_age_top}이 많이 유기되고 있으며, 이는 입양 후 관리 부담이나 나이 관련 요인이 원인일 수 있습니다.<br>"
    if total_cat>0:
        insight_html += f"🐱 고양이: 주로 {cat_age_top}이 많이 유기되고 있으며, 이는 환경 변화 및 돌봄 부담 등이 원인일 수 있습니다.<br>"

    insight_html += "</div>"
    st.markdown(insight_html, unsafe_allow_html=True)




