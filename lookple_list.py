import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

main_url = "https://lookple.com/category/top/26/"


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_list, size_dic_list = [], [], [], [], []

def get_list(url):
  driver.get(url)
  driver.implicitly_wait(time_to_wait=5)
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")
  list_page = soup.select(".prdList.grid3")

  for li in list_page:
    divs = li.find_all(attrs={'class': "thumbnail"})
    for div in divs:
      prd_div = div.find('div', class_='prdImg')
      if prd_div:
        link_list.append("https://lookple.com" + prd_div.find('a')['href'])
        name_list.append(prd_div.find('img')['alt'])
        img_list.append(prd_div.find('img')['src'])
  
  return "complete getting list data"

def get_size(link_list,name_list):
  url = link_list
  driver.get(url)
  driver.implicitly_wait(time_to_wait=5)
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")

  div_tags = soup.find_all('div', style=lambda value: value and 'text-align: center;' in value)
  for div in div_tags:
    if "총장" in div.text.strip():
      size_list.append(div.text.strip())  
  save_size(name_list, size_list)
  return "complete getting size data"

def save_size(name_list, size_list):
  test_dic = {name_list: None}
  temp_size_list = list()
  for i in size_list:
    print(i)
    temp_size_list.append(i)
    break
  test_dic = {name_list:temp_size_list}
  size_dic_list.append(test_dic)
  return "complete save data"

print(get_list(main_url))
print(get_size(link_list[2], name_list[2]))
print(size_dic_list)

import re
def parse_description(description):
    clean_description = re.sub(r'[^0-9가-힣\s]', '', description)
    parts = re.split(r'\s+', clean_description)
    name = parts[0]
    measurements = parts[1:]
    if '어깨' in description:
        size_values = [measurements[1], measurements[3], None, measurements[5], measurements[7], measurements[9]]
    else:
        size_values = [measurements[1], measurements[3], None, measurements[5], measurements[7], measurements[9]]
    
    return [name] + size_values

converted_size_dic_list = []

for item in size_dic_list:
    new_item = {}
    for key, value in item.items():
        descriptions = re.split(r'(?<=\d)(?=[가-힣]+\s*:)', value[0])
        new_value = [parse_description(desc.strip()) for desc in descriptions]
        new_item[key] = new_value
    converted_size_dic_list.append(new_item)

print(converted_size_dic_list)




# DB저장을 위한 데이터 정제








