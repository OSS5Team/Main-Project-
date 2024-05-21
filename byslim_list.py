import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
import psycopg2
from psycopg2 import sql
import pandas as pd
from sqlalchemy import create_engine

main_url = "https://www.byslim.com/category/top/6/"


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_dic_list = [], [], [], []


# 상품 리스트 데이터 가져오기
def get_list(url):
  driver.get(url)
  driver.implicitly_wait(time_to_wait=5)
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")
  # prdList.grid3 class 선택 후 html소스 코드 가져오기
  list_page = soup.select(".prdList.grid3")

  for li in list_page:
    # find_all메소드를 통해 thumbnail 클래스 코드 전부 가져오기
    divs = li.find_all(attrs={'class': "thumbnail"})
    for div in divs:
      # 상위 태크인 prdImg 태그의 하위 태그 값들 가져오기
      prd_div = div.find('div', class_='prdImg')
      if prd_div:
        link_list.append("https://www.byslim.com/" + prd_div.find('a')['href'])
        name_list.append(prd_div.find('img')['alt'])
        img_list.append(prd_div.find('img')['src'])
  
  return "complete getting list data"

def get_size(link_list,name_list):
  size_list = list()
  url = link_list
  driver.get(url)
  driver.implicitly_wait(time_to_wait=5)
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")

  # td 테그 모두 가져오기
  td_tags = soup.find_all("td")
  for td in td_tags:
      if 'style' in td.attrs:
          if td.text.strip()[0] == "착":
              break 
          else: 
              size_list.append(td.text.strip())
  # size 데이터를 저장한 후 save_size 함수 실행
  save_size(name_list, size_list)
  return "complete getting size data"
              
def save_size(name_list, size_list):
  test_dic = {name_list: None}
  temp_size_list = list()
  for i in size_list:
    if '(' in str(i):
      temp_size_list.append(size_list[size_list.index(i):size_list.index(i)+7])
  test_dic = {name_list:temp_size_list}
  # dictionary 형태로 데이터 저장하기
  size_dic_list.append(test_dic)
      


print(get_list(main_url))
print(len(name_list))
print(len(img_list))
print(len(link_list))



for index in range(59):
   get_size(link_list[index], name_list[index])


def check_size_data(d):
  for key, value in d.items():
      print(f'{key}: {value}')

for j in range(3):
  check_size_data(size_dic_list[j])
  print(name_list[j])
  print(img_list[j])
  print(link_list[j])
  print()
  print()
  print()


data = {
  'Name' : name_list,
  'Img' : img_list,
  'Link' : link_list,
}

product_df = pd.DataFrame(data)

# 데이터를 담을 리스트 초기화
data = []

# size_dic_list를 순회하면서 데이터 수집
for dic in size_dic_list:
    for name, sizes in dic.items():
        for size_info in sizes:
            row = [name] + size_info
            data.append(row)

# 데이터프레임 생성
columns = ['Name', 'Size', 'Shoulder Width', 'Chest Circumference', 'Hem Width', 'Sleeve Length', 'Sleeve Opening', 'Total Length']
size_info_df = pd.DataFrame(data, columns=columns)


host = "localhost"
database = "test"
user = "Test"
password = "1234"
   

try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    print("연결 성공!")

except psycopg2.Error as e:
    print("연결 실패:", e)


connection_string = f'postgresql://{user}:{password}@{host}/{database}'

# SQLAlchemy 엔진 생성 (engine 정의)
engine = create_engine(connection_string)
# 데이터프레임을 PostgreSQL에 쓰기
product_table_name = 'byslim_products'
size_info_table_name = 'byslim_size_info'

# product_df 쓰기
with engine.connect() as connection:
    product_df.to_sql(product_table_name, connection, if_exists='replace', index=False, schema='public')

# size_info_df 쓰기
with engine.connect() as connection:
    size_info_df.to_sql(size_info_table_name, connection, if_exists='replace', index=False, schema='public')

print("데이터프레임을 PostgreSQL 테이블로 성공적으로 저장하였습니다.")


# 데이터 프레임 PostgreSQL에 저장
## 주석 달기 및 사이즈 데이터 저장 함수 테스트 및 확인