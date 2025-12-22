import requests
from bs4 import BeautifulSoup

# 1. 웹 페이지 가져오기
url = "https://terms.naver.com/entry.naver?docId=1082254&cid=40942&categoryId=31951"
response = requests.get(url)

# 2. HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 3. 원하는 내용 찾기 (본문 내용)
content = soup.find("div", class_="size_ct_v2")

# 4. 출력
print(content.get_text(strip=True))
