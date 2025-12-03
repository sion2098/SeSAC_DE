# =========================
# 0. 라이브러리 불러오기
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

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
tab1, tab2, tab3 = st.tabs(["동물 종류 & 품종", "장소 패턴", "시기 분석"])

# =========================
# 3-1. 첫 번째 탭: 동물 종류 & 품종 분석
# =========================
import altair as alt  # Altair 추가

with tab1:
    st.header("유기 동물 종류 및 품종 분석")

    # 좌측 그래프, 우측 리스트
    col1, col2 = st.columns([1.5, 1])

    # --------------------------------------------------
# 📌 좌측: 동물 종류별 수 그래프 (Altair 버전)
# --------------------------------------------------
with col1:
    st.subheader("유기 동물 종류별 수")

    # 1) upKindNm 값을 '강아지 / 고양이 / 기타'로 변환
    def kind_group(kind):
        if kind == "개":
            return "강아지"
        elif kind == "고양이":
            return "고양이"
        else:
            return "기타"

    df["kind_group"] = df["upKindNm"].apply(kind_group)

    # 2) 그룹별 수 집계
    kind_counts = df["kind_group"].value_counts().reset_index()
    kind_counts.columns = ["kind_group", "count"]

    # 3) Altair 바 차트 생성
    base = alt.Chart(kind_counts).encode(
        x=alt.X("kind_group:N", axis=alt.Axis(labelAngle=0)),  # 카테고리 이름 그대로 표시
        y=alt.Y("count:Q")
    )

    bar = base.mark_bar()

    # 4) 막대 위 숫자 표시
    text = base.mark_text(
        align="center",
        baseline="bottom",
        dy=-2,
        fontSize=14
    ).encode(
        text="count:Q"
    )

    chart = (bar + text).properties(height=350)

    st.altair_chart(chart, use_container_width=True)


    # --------------------------------------------------
    # 📌 우측: 강아지/고양이 품종 TOP3 – 카드 UI
    # --------------------------------------------------
    with col2:

        # 카드 디자인용 CSS
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

        st.subheader("상위 품종 Top 3")

        # 🔹 강아지 TOP 3
        dog_top3 = df[df["upKindNm"] == "개"]["kindNm"].value_counts().head(3)

        # 🔹 고양이 TOP 3
        cat_top3 = df[df["upKindNm"] == "고양이"]["kindNm"].value_counts().head(3)

        # ===========================
        # 🐶 강아지 카드
        # ===========================
        dog_html = "<div class='animal-card'>"
        dog_html += "<div class='animal-title'>🐶 강아지 TOP 3</div>"
        for idx, (breed, count) in enumerate(dog_top3.items(), start=1):
            dog_html += f"<div class='breed-item'>{idx}. {breed} — {count}건</div>"
        dog_html += "</div>"

        st.markdown(dog_html, unsafe_allow_html=True)

        # ===========================
        # 🐱 고양이 카드
        # ===========================
        cat_html = "<div class='animal-card'>"
        cat_html += "<div class='animal-title'>🐱 고양이 TOP 3</div>"
        for idx, (breed, count) in enumerate(cat_top3.items(), start=1):
            cat_html += f"<div class='breed-item'>{idx}. {breed} — {count}건</div>"
        cat_html += "</div>"

        st.markdown(cat_html, unsafe_allow_html=True)



# =========================
# 3-2. 두 번째 탭: 유기 장소 패턴 분석 (지도 전체 데이터 기준)
# =========================
with tab2:
    st.header("지역별 유기동물 분포 지도")

    # 1. 시/도별 유기동물 수 집계 및 비율 계산 (이전 코드와 동일)
    province_counts = df['province'].value_counts().reset_index()
    
    province_counts.columns = ['province', 'count']
    
    total_animals = len(df)
    province_counts['percent'] = province_counts['count'] / total_animals * 100
    

    # 2. 종별 개수 계산 (피벗 테이블)
    # df의 province와 upKindNm을 기준으로 각 province별 종 개수를 계산합니다.
    species_counts = df.pivot_table(
        index='province',
        columns='upKindNm',
        aggfunc='size',
        fill_value=0
    )
    # 컬럼 이름이 '개', '고양이', '기타' 등으로 되어 있다고 가정합니다.

    # 3. 데이터 병합
    # total_counts에 종별 개수 데이터를 province를 기준으로 left join합니다.
    # 이렇게 하면 province_counts에 있는 16개 행이 모두 유지됩니다.
    province_counts = province_counts.merge(
        species_counts, 
        on='province', 
        how='left'
    ).fillna(0) # merge 후 혹시라도 없는 종 데이터는 0으로 채웁니다.
    
    # province_counts의 dtype을 int로 변환 (count 및 종별 카운트)
    cols_to_convert = ['count'] + list(species_counts.columns)
    for col in cols_to_convert:
        if col in province_counts.columns:
             # 데이터가 float으로 변환되었을 수 있으므로 int로 변환
            province_counts[col] = province_counts[col].astype(int) 

# 🔑 핵심 수정 2: 지도 좌표 매칭의 안전성을 위해 'province' 이름 순서로 명시적 정렬
    # 이 단계를 통해 'count'를 기준으로 한 초기 정렬(value_counts)이 해제됩니다.
    province_counts = province_counts.sort_values(by='province').reset_index(drop=True)
    
    # 4. 지도 생성 및 마커 추가 (이전 코드와 동일)
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    province_coords = {
        # ... (province_coords는 그대로 사용)
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
    
    # 마커 추가
    for idx, row in province_counts.iterrows():
        prov = row['province']
        
        # ⚠️ 중요: province_counts에 있는 province가 province_coords에 없는 경우 스킵
        if prov not in province_coords:
            # st.warning(f"경고: {prov}의 좌표 정보가 누락되었습니다.") 
            continue 
        # print(row)
        # 팝업 텍스트에서 .get()을 사용하여 데이터 누락에 안전하게 대응
        popup_text = f"""
        <b>{prov}</b><br>
        총 유기동물 수: {row['count']} ({row['percent']:.1f}%)<br>
        강아지: {row.get('개', 0)}<br>
        고양이: {row.get('고양이', 0)}<br>
        기타: {row.get('기타', 0)}
        """
        
        # 'count' 값이 0일 경우 반경이 너무 작아지므로 최소 반경을 설정
        radius = 10 + row['count'] / 500
        
        folium.CircleMarker(
            location=province_coords[prov],
            radius=radius,
            color='blue',
            fill=True,
            fill_color='skyblue',
            fill_opacity=0.6,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)
    
    # 지도 표시
    st_folium(m, width=700, height=500)

# =========================
# 3-3. 세 번째 탭: 유기 시기 분석 (필터링 적용)
# =========================
with tab3:
    st.header("시기 분석")
    
    # -------------------------
    # 1) 날짜 필터
    # -------------------------
    start_date = st.date_input("시작 날짜", df["happenDt"].min())
    end_date = st.date_input("종료 날짜", df["happenDt"].max())
    
    filtered_df = df[(df["happenDt"] >= pd.to_datetime(start_date)) & 
                     (df["happenDt"] <= pd.to_datetime(end_date))]
    
    filtered_df = filtered_df.sort_values(by="happenDt", ascending=True)  # 오래된 날짜 순 정렬
    st.markdown(f"### 필터 적용 후 데이터 수: {len(filtered_df)}개")
    # st.dataframe(filtered_df) 
    
    # -------------------------
    # 2) 월/계절 컬럼 추가
    # -------------------------
    filtered_df['happenDt'] = pd.to_datetime(filtered_df['happenDt'])
    filtered_df['month'] = filtered_df['happenDt'].dt.month
    
    # 계절 컬럼 만들기
    def get_season(month):
        if month in [3,4,5]:
            return '봄'
        elif month in [6,7,8]:
            return '여름'
        elif month in [9,10,11]:
            return '가을'
        else:
            return '겨울'
    filtered_df['season'] = filtered_df['month'].apply(get_season)
    
    # -------------------------
    # 3) 종별 카테고리화 (강아지/고양이)
    # -------------------------
    filtered_df = filtered_df[filtered_df['upKindNm'].isin(['개','고양이'])]
    
    # =========================
    # 월별 유기동물 발생 건수 (강아지/고양이 그룹 막대)
    # =========================
    monthly_species_counts = filtered_df.groupby(['month','upKindNm']).size().reset_index(name='count')
    
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.barplot(
        data=monthly_species_counts,
        x='month',
        y='count',
        hue='upKindNm',
        palette={'개':'skyblue','고양이':'lightgreen'},
        ax=ax1
    )
    ax1.set_title("월별 유기동물 발생 건수 (강아지/고양이)")
    ax1.set_xlabel("월")
    ax1.set_ylabel("건수")
    ax1.set_xticks(range(filtered_df['month'].min(), filtered_df['month'].max()+1))
    st.pyplot(fig1)
    
    # =========================
    # 계절별 유기동물 발생 건수 (강아지/고양이 그룹 막대)
    # =========================
    seasonly_species_counts = filtered_df.groupby(['season','upKindNm']).size().reset_index(name='count')
    
    fig2, ax2 = plt.subplots(figsize=(8,5))
    sns.barplot(
        data=seasonly_species_counts,
        x='season',
        y='count',
        hue='upKindNm',
        palette={'개':'skyblue','고양이':'lightgreen'},
        ax=ax2
    )
    ax2.set_title("계절별 유기동물 발생 건수 (강아지/고양이)")
    ax2.set_xlabel("계절")
    ax2.set_ylabel("건수")
    st.pyplot(fig2)
    
    # -------------------------
    # 4) 계절별 최대 발생 확인
    # -------------------------
    season_counts = filtered_df['season'].value_counts().reindex(['봄','여름','가을','겨울'])
    max_season = season_counts.idxmax()
    st.markdown(f"💡 **분석:** 유기 동물이 가장 많이 발생하는 계절은 **{max_season}**입니다.")

    
    # # 월별 유기 동물 수
    # st.subheader("월별 유기 동물 수")
    # month_counts = filtered_df["month"].value_counts().sort_index()
    # st.bar_chart(month_counts)
    
    # # 요일별 유기 동물 수
    # st.subheader("요일별 유기 동물 수")
    # weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    # weekday_counts = filtered_df["weekday"].value_counts().reindex(weekday_order)
    # st.bar_chart(weekday_counts)
    
    # # 나이 분포
    # st.subheader("나이(개월) 분포")
    # fig1, ax1 = plt.subplots()
    # sns.histplot(filtered_df["age_months"].dropna(), bins=20, kde=True, ax=ax1)
    # st.pyplot(fig1)
    
    # # 체중 분포
    # st.subheader("체중(Kg) 분포")
    # fig2, ax2 = plt.subplots()
    # sns.histplot(filtered_df["weight"].dropna(), bins=20, kde=True, ax=ax2)
    # st.pyplot(fig2)
    
    # # 성별 분포
    # st.subheader("성별 분포")
    # st.bar_chart(filtered_df["sexCd"].value_counts())

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
