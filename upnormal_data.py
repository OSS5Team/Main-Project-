import requests
from bs4 import BeautifulSoup

# 대상 웹페이지 URL
url = 'https://upnormal.kr/category/outer/24/'

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
    product_list = soup.find_all('ul', class_='xans-element- xans-product xans-product-listitem spec')

    if product_list:
        # 각 제품을 순회하면서 정보 추출
        for product in product_list:
            # 제품 가격 추출
            price_tag = product.find('li', title='판매가')
            product_price = price_tag.text.strip() if price_tag else 'No price found'

            # 상품 요약 정보 추출
            summary_tag = product.find('li', title='상품요약정보')
            product_summary = summary_tag.text.strip() if summary_tag else 'No summary found'

            # 사용 후기 추출
            review_tag = product.find('li', title='사용후기')
            product_review = review_tag.text.strip() if review_tag else 'No review found'

            # 상품 문의 추출
            question_tag = product.find('li', title='상품문의')
            product_question = question_tag.text.strip() if question_tag else 'No question found'

            # 추출한 정보 출력
            print(f'가격: {product_price}')
            print(f'요약 정보: {product_summary}')
            print(f'사용 후기: {product_review}')
            print(f'상품 문의: {product_question}')
            print('-' * 20)
    else:
        print('제품 리스트를 찾을 수 없습니다.')
else:
    print('웹페이지를 불러오는데 실패했습니다. 상태 코드:', response.status_code)
