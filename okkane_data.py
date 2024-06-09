import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL 가져오기
url = "https://www.okkane.co.kr/shop/shopbrand.html?xcode=073&type=Y"

# URL에서 HTML 가져오기
response = requests.get(url)
html = response.content

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html, "html.parser")

# 의류 데이터 추출
items = soup.find_all("dd", class_="")

# 데이터 저장을 위한 리스트 생성
data = []

for item in items:
    # 상품명 추출
    product_name_element = item.find("li", class_="names")
    if product_name_element and product_name_element.a:
        product_name = product_name_element.a.text.strip()
    else:
        product_name = ""

    # 색상 정보 추출
    colors = item.find("li", class_="colorbox")
