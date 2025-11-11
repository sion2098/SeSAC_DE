import requests  # 웹 페이지 요청을 위해 import
                                # 가져온 문서에서 데이터 추출을 위해 import 
from bs4 import BeautifulSoup   # bs4에 BeautifulSoup이라는 class가 있음

#크롤링하고자 하는 url을 받을 변수를 생성
url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)  # URL 요청에 대한 응답(결과값)을 받아 response에 할당
                                    #응답으로 받은 결과 > HTML 문서 텍스트를 가져와 bs 객체로 생성
bs = BeautifulSoup(response.text)  #크롤링 작업을 bs 객체를 통해 수행

'''andorra = bs.select_one("h3.country-name") #웹 페이지에서 모든 나라 이름이 h3.countey-name으로 지정되어 있어 select로 하면 모든 나라 이름 불러옴
#print(andorra.get_text(strip=True)) #andorra에서 실제 텍스트만 가져옴  #strip=True :  앞뒤 공백 문자 제거

country = bs.select_one("div.row div.col-md-4.country")
print(country)'''

countries = bs.select("div.row div.col-md-4")

for country in countries:
    print(country.select_one("h3.country-name").get_text(strip=True))
    country_info = country.select_one("div.country-info")
    capital = country_info.select_one("span.country-capital").get_text(strip=True)
    population = country_info.select_one("span.country-population").get_text(strip=True)
    area = country_info.select_one("span.country-area").get_text(strip=True)
    print(f"수도 : {capital}, 인구 : {population}, 면적 : {area}")

