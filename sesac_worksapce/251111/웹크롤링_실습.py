import requests
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/e-commerce/static/phones/touch"
res = requests.get(url)
bs = BeautifulSoup(res.text)

# 이미지 url 가져오기
product_info = bs.select("div.row div.col-md-4.col-xl-4.col-lg-4")
pd_img = bs.select_one("img[itemprop='image']")
print(pd_img.get("src"))

# 상품 이름 가져오기
pd_name = bs.select_one("h4 a.title")
print(pd_name.get_text(strip=True))

# 상품 가격 가져오기
pd_price = bs.select_one("span[itemprop='price']")
print(pd_price.get_text(strip=True))

#상세 스펙 텍스트 가져오기
pd_spec = bs.select_one("p.description.card-text")
print(pd_spec.get_text(strip=True))

#리뷰 개수
pd_review = bs.select_one("p.review-count.float-end")
print(pd_review.get_text(strip=True))

#별의 개수(선택)
pd_star = bs.select_one("p[data-rating]")
print(pd_star.get("data-rating"))

# 각 상품의 상세 페이지 주소 url(선택)
pd_link = bs.select_one("h4 a.title[href]")  # a태그의 title 클래스 안에 있는 속성 href # 클래스 안에 있는 속성값을 찾는거라 대괄호[]안에 작성
print(pd_link.get("href"))