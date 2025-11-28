# 필요한 라이브러리
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# 1. 웹 크롤링 (예시: Booking 스타일)
# ------------------------------
def crawl_booking(city_url):
    hotels = []
    # 예시: city_url은 Booking 서울 호텔 검색 결과 페이지
    response = requests.get(city_url)

    print(response)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 호텔 정보 추출 (HTML 구조에 따라 클래스명 조정 필요)
    hotel_list = soup.find_all('div', class_='sr_item')
    for h in hotel_list:
        name = h.find('span', class_='sr-hotel__name').text.strip()
        price = h.find('div', class_='bui-price-display__value')
        price = int(price.text.replace('$','').replace(',','')) if price else None
        rating = h.find('div', class_='bui-review-score__badge')
        rating = float(rating.text.strip()) if rating else None
        review_count = h.find('div', class_='bui-review-score__text')
        review_count = int(review_count.text.strip().split()[0].replace(',','')) if review_count else None
        
        hotels.append({
            'platform': 'Booking',
            'hotel_name': name,
            'price_usd': price,
            'rating': rating,
            'review_count': review_count
        })
    return hotels

# # ------------------------------
# # 2. 크롤링된 데이터 DataFrame으로 변환
# # ------------------------------
# 예시 URL (실제 프로젝트 시 적절한 URL 필요)
booking_url = 'https://www.booking.com/searchresults.ko.html?ss=%EC%98%A4%EB%A6%AC%EC%97%94%EC%8A%A4+%ED%98%B8%ED%85%94+%26+%EB%A0%88%EC%A7%80%EB%8D%98%EC%8A%A4+%EB%AA%85%EB%8F%99%2C+%EC%84%9C%EC%9A%B8%2C+%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD&efdco=1&label=naver-gW3gsa0TCFDHapd5rcFpDQ&aid=2375413&lang=ko&sb=1&src_elem=sb&src=index&dest_id=1296885&dest_type=hotel&ac_position=0&ac_click_type=b&ac_langcode=ko&ac_suggestion_list_length=1&search_selected=true&search_pageview_id=04192d65895a0318&ac_meta=GhAwNDE5MmQ2NTg5NWEwMzE4IAAoATICa286FOyYpOumrOyXlOyKpCDtmLjthZQgQABKAFAA&checkin=2025-12-15&checkout=2025-12-18&group_adults=2&no_rooms=1&group_children=0'
booking_data = crawl_booking(booking_url)


# ------------------------------
# 3. Expedia 데이터도 동일 방식 크롤링
# ------------------------------
# 크롤링 함수 작성 후 동일한 방식으로 DataFrame 생성
# df_expedia = pd.DataFrame(expedia_data)

# ------------------------------
# 4. 데이터 병합 (호텔명 기준)
# ------------------------------
# 하루 프로젝트용: Booking과 Expedia 데이터 샘플
df_expedia = df_booking.copy()
df_expedia['platform'] = 'Expedia'
df_expedia['price_usd'] = df_expedia['price_usd'] * 1.05  # 예시: 가격 약간 다르게

df_all = pd.concat([df_booking, df_expedia], ignore_index=True)

# ------------------------------
# 5. 분석 예시
# ------------------------------
# 플랫폼별 평균 가격
platform_avg = df_all.groupby('platform')['price_usd'].mean().reset_index()
print(platform_avg)

# 동일 호텔 가격 비교
df_pivot = df_all.pivot_table(index='hotel_name', columns='platform', values='price_usd')
df_pivot['price_diff'] = df_pivot['Booking'] - df_pivot['Expedia']
print(df_pivot.head())

# ------------------------------
# 6. 시각화
# ------------------------------
sns.barplot(x='platform', y='price_usd', data=df_all)
plt.title('Platform Average Price')
plt.show()

sns.scatterplot(x='review_count', y='price_usd', hue='platform', data=df_all)
plt.title('Price vs Review Count')
plt.show()

sns.heatmap(df_pivot[['Booking','Expedia']], annot=True, fmt=".0f", cmap='YlGnBu')
plt.title('Hotel Price Comparison')
plt.show()
