import requests
import json
import pandas as pd

# 1. API 기본 URL
url = "https://api.odcloud.kr/api/FlightStatusListDTL/v1/getFlightStatusListDetail"

# 2. 파라미터
params = {
    "page": 3,
    "perPage": 100,
    "returnType": "JSON",
    "serviceKey": "b6669c292241aeba6e342a03b64a31afa86132b5ee5eb274a36d3bd28b664965"
}

# 3. 요청 보내기
response = requests.get(url, params=params)

# 4. 응답 출력
print("Status Code:", response.status_code)
data = response.json()
print(data)

# data = response
# print(json.dumps(data, indent=4, ensure_ascii=False))

df = pd.DataFrame(data['data'])
pd.set_option('display.max_columns', None)
print(df)
print(df.shape)

