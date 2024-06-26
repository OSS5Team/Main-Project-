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
    if colors:
        color_list = [color.get("style").split(":")[1].strip(";") for color in colors.find_all("span")]
    else:
        color_list = []

    # 사이즈 정보 추출
    size_element = item.find("li", class_="subnames")
    if size_element and size_element.a:
        sizes = size_element.a.text.strip("[]").split(",")
    else:
        sizes = []
    
    # 리뷰 수 추출
    review_count_element = item.find("span", class_="snap_review_count")
    if review_count_element:
        review_count = review_count_element.text
    else:
        review_count = ""
    
    # 가격 정보 추출
    price_element = item.find("li", class_="prices")
    if price_element:
        price = price_element.text.strip("원")
    else:
        price = ""

    # 추가 정보 추출
    extra_info_element = item.find("div", class_="item_de")
    if extra_info_element:
        extra_info = extra_info_element.text.strip()
    else:
        extra_info = ""

    
    # 데이터 리스트에 추가
    data.append({
        "상품명": product_name,
        "색상": ", ".join(color_list),
        "사이즈": ", ".join(sizes),
        "리뷰 수": review_count,
        "가격": price,
        "추가 정보": extra_info
    })

# 데이터프레임 생성
df = pd.DataFrame(data)

# 데이터프레임 출력 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# 데이터프레임 출력
print(df)

