import requests
import pandas as pd

# 컬럼 전체 출력
pd.set_option('display.max_columns', None)

# API 요청 정보
url = "https://apis.data.go.kr/1613000/ExpflightInfoService/getFlightOpratInfoList"  # 예시 URL
service_key = "b6669c292241aeba6e342a03b64a31afa86132b5ee5eb274a36d3bd28b664965"  # 실제 인증키로 바꾸세요

# 일본 주요 공항 코드 (예시)
japan_airports = ['NRT', 'HND', 'KIX', 'CTS', 'FUK', 'NGO', 'OKA']  

# 요청 파라미터
params = {
    'serviceKey': service_key,
    'numOfRows': 50,       # 최대 데이터 수
    'pageNo': 1,
    'depAirportId': 'ICN',   # 출발 공항: 인천
    'schDate': '20251203',    # 조회할 날짜 YYYYMMDD
    'type': 'json'
}

# API 요청
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # 실제 데이터가 있는 부분 접근 (API 구조에 따라 수정 필요)
    items = data['response']['body']['items']['item']
    
    # DataFrame 생성
    df = pd.DataFrame(items)
    
    # 일본 공항만 필터링
    df_japan = df[df['ARRIVED_ENG'].isin(japan_airports)]
    
    # 결과 출력
    print(df_japan)
    print(f"\n총 {len(df_japan)}건")
else:
    print("API 요청 실패:", response.status_code)
