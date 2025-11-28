import requests
from bs4 import BeautifulSoup
from pprint import pprint



for page in range(1,3):
    url = f"https://books.toscrape.com/catalogue/category/books/childrens_11/page-{page}.html"
    res = requests.get(url)
    bs = BeautifulSoup(res.text)

    book = bs.select("ol.row article.product_pod")
    genre = bs.select_one("div.page-header.action h1").get_text(strip=True)
    print(f"장르 : {genre}")

    if not book:  #마지막 페이지면 중단
        break

    book_list = []     # 페이지별로 초기화

    for book_info in book: 

        b_title = book_info.select_one("h3 a[title]").get_text(strip=True) #<h3> 안 <a> 중 title 속성이 있는 것 선택 / ("h3 a")해도 출력됨 : h3 태그 안에 있는 a 태그를 선택 a의 속성 title까지 접근 가능
        b_price = book_info.select_one("p.price_color").get_text(strip=True)
        b_img_url = book_info.select_one("div.image_container img")["src"]
        b_detail_url = book_info.select_one("h3 a")["href"]
        b_star = book_info.select_one("p.star-rating")["class"]
        star = b_star[1]

        book_list.append(
            {
                "책 제목" : b_title,
                "책 가격" : b_price,
                "별점" : star,
                "이미지 주소" : b_img_url,
                "상세페이지 주소" : b_detail_url
            }
        )

    print(f"\n==================== {page}페이지 ======================")
    pprint(book_list)
    print(f"이 페이지 책 개수: {len(book_list)}")
