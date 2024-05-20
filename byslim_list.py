import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd


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



for index in range(3):
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

df = pd.DataFrame(data)

print(df)


data_rows = []
def dataframe_dictionary(dictionary):
    for name, sizes in dictionary.items():
        for size_info in sizes:
            size = size_info[0]
            size_numbers = size_info[1:]
            data_rows.append([name, size, ', '.join(size_numbers)])

for i in range(3):
  dataframe_dictionary(size_dic_list[i])

df = pd.DataFrame(data_rows, columns=['name', 'size', 'size_number'])
print(df)







