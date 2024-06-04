import requests
from bs4 import BeautifulSoup

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
    product_list = soup.find_all('div', class_='description')

    if product_list:
        # 각 제품을 순회하면서 정보 추출
        for product in product_list:
            # 제품명 추출
            name_tag = product.find('strong', class_='name')
            product_name = name_tag.text.strip() if name_tag else 'No name found'

            # 제품 가격 추출
            price_tag = product.find('li', attrs={'rel': '판매가'})
            product_price = price_tag.find('span').text.strip() if price_tag else 'No price found'

            # 상품 요약 정보 추출
            summary_tag = product.find('li', attrs={'rel': '상품요약정보'})
            product_summary = summary_tag.text.strip() if summary_tag else 'No summary found'

            # 추출한 정보 출력
            print(f'제품명: {product_name}')
            print(f'가격: {product_price}')
            print(f'요약 정보: {product_summary}')
            print('-' * 20)
    else:
        print('제품 리스트를 찾을 수 없습니다.')
else:
    print('웹페이지를 불러오는데 실패했습니다. 상태 코드:', response.status_code)
