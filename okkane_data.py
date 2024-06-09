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
