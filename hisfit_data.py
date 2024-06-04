import requests
from bs4 import BeautifulSoup
import re

# 대상 웹페이지 URL
url = 'https://hisfit.co.kr/category/outer/24/'

# 사용자 에이전트 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 웹사이트에 GET 요청 보내기
response = requests.get(url, headers=headers)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # 페이지의 HTML 내용을 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제품 정보를 담고 있는 컨테이너 찾기
    products = soup.find_all('div', class_='description')

    if products:
        # 각 제품을 순회하면서 정보 추출
        for product in products:
            # 제품명 추출
            name_tag = product.find('strong', class_='name')
            name = name_tag.text.strip() if name_tag else '상품명 없음'

            # 가격 추출
            price_tag = product.find('li', rel='판매가')
            price_span = price_tag.find('span', style='font-size:12px;color:#101010;font-weight:bold;')
            price_text = price_span.text.strip() if price_span else '가격 정보 없음'
            price = re.findall(r'\d+', price_text)  # 숫자만 추출
            price = ''.join(price) if price else '가격 정보 없음'

            # 상품 요약 정보 추출
            summary_tag = product.find('li', rel='상품요약정보')
            summary_span = summary_tag.find('span', style='font-size:12px;color:#aaaaaa;')
            summary = summary_span.text.strip() if summary_span else '요약 정보 없음'

            # 이미지 URL 추출
            image_tag = product.find('img')
            image_url = image_tag['src'] if image_tag else '이미지 없음'

            # 출력
            print("상품명:", name)
            print("판매가:", price)
            print("상품 요약 정보:", summary)
            print("이미지 URL:", image_url)
            print('-' * 50)
    else:
        print('제품 정보를 찾을 수 없습니다.')
else:
    print('웹페이지를 불러오는데 실패했습니다. 상태 코드:', response.status_code)
