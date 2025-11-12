# selenium 및 webdriver 라이브러리 불러오기
from selenium import webdriver
# 화면 꺼지지 않게 유지
from selenium.webdriver.chrome.options import Options 
# By 라이브러리 불러오기
from selenium.webdriver.common.by import By
# time 라이브러리 불러오기
import time
from selenium.webdriver.common.keys import Keys
# Selenium에서 기다리는 기능 (로딩 기다릴 때 사용)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# BeautifulSoup: HTML 안에서 글자나 태그를 뽑는 도구
from bs4 import BeautifulSoup


# 1. 브라우저 실행
driver = webdriver.Chrome() #크롬 열기
driver.get("https://quotes.toscrape.com/scroll") #해당 url 주소로 이동

# 2. 무한 스크롤 (Selenium 역할)
# driver.execute_script(SCRIPT) : 웹 브라우저에 JavaScript를 동적으로 실행
last_height = driver.execute_script("return document.body.scrollHeight") #지금 화면의 가장 아래 높이를 가져옴
while True : #스크롤 끝까지 내릴때까지 반복
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #화면을 제일 아래로 내리기
    time.sleep(1.5)
    new_height = driver.execute_script("return document.body.scrollHeight") #스크롤 후 새로운 높이 확인
    if new_height == last_height: #만약 높이가 같으면 멈춤(더 이상 스크롤 되지 않을때)
        break
    last_height = new_height #다음 반복을 위해 높이 갱신

# 3. 로딩 완료 대기
WebDriverWait(driver, 5).until( 
    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
)

# 4. 현재 페이지 HTML 가져오기(Selenium -> BeautifulSoup 전달)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 5. BeautifulSoup으로 데이터 추출
quotes = soup.select(".quote") #HTML 안에서 "quote"라는 부분 찾기

for q in quotes[:5]:
    text = q.select_one(".text").get_text(strip=True)
    author = q.select_one(".author").get_text(strip=True)
    print(f'"{text}"-{author}') # 출력: 명언과 누가 말했는지

driver.quit() # 다 끝나면 브라우저 닫기