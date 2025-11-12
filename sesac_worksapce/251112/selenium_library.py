# selenium 및 webdriver 라이브러리 불러오기
from selenium import webdriver
# 화면 꺼지지 않게 유지
from selenium.webdriver.chrome.options import Options 
# By 라이브러리 불러오기
from selenium.webdriver.common.by import By
# time 라이브러리 불러오기
import time
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://naver.com"
driver.get(url)  # 해당 url로 접속하기
time.sleep(1) #1초 대기 후 다음 코드 실행

# 검색어 입력
# 로케이터 = 뭘로 검색할것인지 지정(By.ID)
query = driver.find_element(By.ID, "query") #fin_element() 함수로 id 속성이 'query'인 요소 반환
query.send_keys("데이터 엔지니어링") # 입력하고 싶은 문자 입력
time.sleep(1)

#엔터 입력 -> 위에 입력값에 대해서 엔터키 누르는 거니까 위에 query 이용하면 됨
query.send_keys(Keys.ENTER)


'''search_btn = driver.find_element(By.CSS_SELECTOR, "#search-btn") #아이디 선택자 -> #id { color : red; }
# By.ID로 입력할 경우 : find_element(By.ID, "search-btn")
search_btn.click() # 버튼 클릭하는 동작 지정'''