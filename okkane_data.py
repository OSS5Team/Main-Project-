import requests
from bs4 import BeautifulSoup

# URL 가져오기
url = "https://www.okkane.co.kr/shop/shopbrand.html?xcode=073&type=Y"

# URL에서 HTML 가져오기
response = requests.get(url)
html = response.content

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html, "html.parser")

# 의류 데이터 추출
items = soup.find_all("dd")

for item in items:
# 색상 정보 추출
    colors = item.find("li", class_="colorbox")
    color_list = [color.get("style").split(":")[1].strip(";") for color in colors.find_all("span")]

 # 상품명, 사이즈 정보 추출
    names = item.find("li", class_="names")
    subnames = item.find("li", class_="subnames")
    product_name = names.a.text.strip()
    sizes = subnames.a.text.strip("[]").split(",")

    # 리뷰 수 추출
    review_count = item.find("span", class_="snap_review_count").text

    # 가격 정보 추출
    price = item.find("li", class_="prices").text.strip("원")

    # 데이터 출력
    print("상품명:", product_name)
    print("색상:", ", ".join(color_list))
    print("사이즈:", ", ".join(sizes))
    print("리뷰 수:", review_count)
    print("가격:", price)
    print("---")
