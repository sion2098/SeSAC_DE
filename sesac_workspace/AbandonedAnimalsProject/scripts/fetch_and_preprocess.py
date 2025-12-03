# import requests  # API 호출 라이브러리
# import pandas as pd  # 데이터 분석 및 데이터프레임 처리 라이브러리
# import os
# from dotenv import load_dotenv

# # # =========================
# # # 0. API 키 불러오기
# # # =========================
# # API_KEY = os.getenv("api_key")  # 인증키

# # # =========================
# # # 1. API 기본 정보
# # # =========================

# API_KEY = "넣기"   # ← 반드시 본인 키 넣기
# ENDPOINT = "https://apis.data.go.kr/1543061/abandonmentPublicService_v2/abandonmentPublic_v2"

# START_DATE = "20250101"  # 조회 시작일
# END_DATE   = "20251203"  # 조회 종료일
# NUM_OF_ROWS = 1000        # 한 번에 가져올 데이터 수
# page_no = 1               # 시작 페이지 번호

# # =========================
# # 2. 전체 데이터를 저장할 리스트 생성
# # =========================
# all_items = []  # 모든 페이지 데이터를 저장할 리스트

# # =========================
# # 3. 페이지 반복 호출
# # =========================
# while True:
#     # API 요청 파라미터 설정
#     params = {
#         "serviceKey": API_KEY,
#         "bgnde": START_DATE,
#         "endde": END_DATE,
#         "pageNo": page_no,     # 현재 페이지
#         "numOfRows": NUM_OF_ROWS,  # 페이지당 데이터 수
#         "_type": "json"        # JSON 형식으로 요청
#     }
    
#     try:
#         response = requests.get(ENDPOINT, params=params)  # API 호출
#         response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
#         data = response.json()  # JSON 응답을 dict로 변환
        
#         # 실제 데이터 리스트 추출
#         items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        
#         if not items:  # 더 이상 데이터가 없으면 반복 종료
#             break
        
#         all_items.extend(items)  # 현재 페이지 데이터를 전체 리스트에 추가
#         print(f"{page_no}페이지 완료, 현재까지 총 {len(all_items)}건 수집됨")
#         page_no += 1  # 다음 페이지로 이동
        
#     except requests.exceptions.HTTPError as err:
#         print("HTTP 오류 발생:", err)
#         break
#     except Exception as e:
#         print("기타 오류 발생:", e)
#         break

# # =========================
# # 4. 전체 데이터를 데이터프레임으로 변환
# # =========================
# df = pd.DataFrame(all_items)  # 전체 데이터를 데이터프레임으로 변환

# # =========================
# # 5. 분석용 컬럼만 선택
# # =========================
# columns_to_keep = [
#     "desertionNo",  # 유기동물 번호
#     "happenDt",     # 유기 발생일
#     "happenPlace",  # 유기 장소
#     "upKindNm",     # 상위 동물 종류 (개/고양이)
#     "kindNm",       # 품종
#     "age",          # 나이
#     "weight",       # 체중
#     "sexCd",        # 성별
#     "neuterYn",     # 중성화 여부
#     "processState", # 보호 상태
#     "careNm",       # 보호소 이름
#     "orgNm",        # 보호소 소속 기관
#     "endReason"     # 보호 종료 사유
# ]

# df = df[columns_to_keep]  # 필요한 컬럼만 남김

# # =========================
# # 6. 날짜 컬럼 형식 변환
# # =========================
# df["happenDt"] = pd.to_datetime(df["happenDt"], format="%Y%m%d")  # 유기 발생일 변환

# # =========================
# # 7. 최종 데이터 확인
# # =========================
# print(f"총 {len(df)}건의 데이터 조회 완료")
# print(df.head())  # 상위 5개 데이터 확인

# # =========================
# # 8. CSV 파일로 저장
# # =========================
# df.to_csv("abandoned_animals_2025.csv",  # 저장할 파일명
#           index=False,                  # 인덱스 번호는 제외
#           encoding="utf-8-sig")         # 한글 깨짐 방지
          
# print("CSV 파일 저장 완료: abandoned_animals_final_2025.csv")



# =========================
# 0. 라이브러리 불러오기
# =========================
import requests          # API 호출
import pandas as pd      # 데이터프레임 처리
import os                # 환경 변수 접근
from dotenv import load_dotenv  # .env 파일에서 API 키 로드

# =========================
# 0-1. API 키 불러오기 (.env 파일 사용 가능)
# =========================
# load_dotenv()  # 필요 시 .env 파일에서 불러오기
# API_KEY = os.getenv("api_key")  # 환경 변수에서 키 불러오기

# =========================
# 1. API 기본 정보
# =========================
API_KEY = "넣기"  # 반드시 본인 키 사용
ENDPOINT = "https://apis.data.go.kr/1543061/abandonmentPublicService_v2/abandonmentPublic_v2"
START_DATE = "20250101"  # 조회 시작일
END_DATE = "20251203"    # 조회 종료일
NUM_OF_ROWS = 1000       # 한 번에 가져올 데이터 수
page_no = 1              # 시작 페이지 번호

# =========================
# 2. 전체 데이터를 저장할 리스트 생성
# =========================
all_items = []  # API에서 가져온 모든 데이터를 저장

# =========================
# 3. API 페이지 반복 호출
# =========================
while True:
    params = {
        "serviceKey": API_KEY,
        "bgnde": START_DATE,
        "endde": END_DATE,
        "pageNo": page_no,
        "numOfRows": NUM_OF_ROWS,
        "_type": "json"
    }

    try:
        response = requests.get(ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()

        # 실제 데이터 리스트 추출
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

        if not items:  # 데이터가 없으면 종료
            break

        all_items.extend(items)
        print(f"{page_no}페이지 완료, 현재까지 총 {len(all_items)}건 수집됨")
        page_no += 1

    except requests.exceptions.HTTPError as err:
        print("HTTP 오류 발생:", err)
        break
    except Exception as e:
        print("기타 오류 발생:", e)
        break

# =========================
# 4. 전체 데이터를 데이터프레임으로 변환
# =========================
df = pd.DataFrame(all_items)

# =========================
# 5. 분석용 컬럼만 선택
# =========================
columns_to_keep = [
    "desertionNo", "happenDt", "happenPlace", "upKindNm", "kindNm", 
    "age", "weight", "sexCd", "neuterYn", "processState", "careNm", "orgNm", "endReason"
]
df = df[columns_to_keep]

# =========================
# 6. 날짜 컬럼 형식 변환
# =========================
df["happenDt"] = pd.to_datetime(df["happenDt"], format="%Y%m%d")

# =========================
# 7. 나이 컬럼 표준화 함수 정의
# =========================
def normalize_age(age_str):
    """
    age 컬럼 문자열을 비교 가능한 형태로 변환
    - '60일미만' → 'baby' (출산 가능성 높은 어린 동물)
    - '2025(년생)' → '2025' (출생년도 기준으로 그룹핑 가능)
    """
    if pd.isna(age_str):
        return None
    if "60일" in age_str:
        return "baby"
    year = age_str.split("(")[0]
    if year.isdigit():
        return year
    return age_str

# =========================
# 8. age_group 컬럼 추가
# =========================
df["age_group"] = df["age"].apply(normalize_age)

# =========================
# 9. 출산 여부 판단 기준으로 그룹핑
# =========================
group_cols = ["happenDt", "happenPlace", "upKindNm", "kindNm", "age_group"]

# 같은 그룹에 3마리 이상 → 출산 그룹으로 판단
group_counts = df.groupby(group_cols).size().reset_index(name="count")
birth_groups = group_counts[group_counts["count"] >= 3]
print("출산으로 판단되는 그룹 수:", len(birth_groups))

# =========================
# 10. 출산 그룹 데이터 제거
# =========================
df_merged = df.merge(
    birth_groups[group_cols],
    on=group_cols,
    how="left",
    indicator=True
)
df_clean = df_merged[df_merged["_merge"] == "left_only"].drop(columns=["_merge"])

print("제거 전 데이터 수:", len(df))
print("제거 후 데이터 수:", len(df_clean))
print("제거된 데이터 수:", len(df) - len(df_clean))

# =========================
# 11. 최종 데이터 확인
# =========================
df = df_clean  # 정제된 데이터로 갱신
print(f"총 {len(df)}건의 데이터 조회 완료")
print(df.head())

# =========================
# 12. 시/도 단위 추출 함수 정의
# =========================
def extract_province(location):
    """
    orgNm 컬럼에서 시/도 단위만 추출
    - '특별시', '광역시', '도' 포함되는 부분까지만 반환
    """
    if pd.isna(location):
        return None
    for keyword in ['특별시', '광역시', '도']:
        if keyword in location:
            idx = location.find(keyword) + len(keyword)
            return location[:idx]
    return location  # 키워드 없으면 전체 반환

# =========================
# 13. province 컬럼 추가
# =========================
df['province'] = df['orgNm'].apply(extract_province)

# 결과 확인
print(df[['orgNm', 'province']].head())

# =========================
# 14. CSV 파일로 저장
# =========================
csv_filename = "abandoned_animals_2025.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
print(f"CSV 파일 저장 완료: {csv_filename}")

# =========================
# 15. 저장된 CSV 파일 간단 확인
# =========================
df_check = pd.read_csv(csv_filename, encoding="utf-8-sig")
print(f"저장된 CSV 파일 '{csv_filename}' 불러오기 완료")
print(df_check.head())
