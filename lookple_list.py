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
print(get_size(link_list[7], name_list[7]))
print(size_dic_list)

import re
def parse_description(description):
    size_names = ['FREE', 'S', 'M', 'L', 'XL', 'XLL']
    name_match = re.match(r'^(FREE|S|M|L|XL|XLL)\s*:', description)
    if name_match:
        name = name_match.group(1)
        measurements = description[len(name_match.group(0)):].strip()
    else:
        name = ""
        measurements = description

    measurement_keywords = ['어깨', '가슴', '소매', '암홀', '총장', '허리', '밑위', '허벅지', '밑단']
    clean_measurements = re.split(r'\s+', measurements)
    
    size_values = [None] * 6  

    keyword_indices = {'어깨': 0, '가슴': 1, '소매': 3, '암홀': 4, '총장': 5, '허리': 6, '밑위': 7, '허벅지': 8, '밑단': 9}

    current_index = 0
    while current_index < len(clean_measurements):
        keyword = clean_measurements[current_index]
        if keyword in keyword_indices:
            index = keyword_indices[keyword]
            if index < len(size_values):
                size_values[index] = clean_measurements[current_index + 1]
            current_index += 2
        else:
            current_index += 1

    return [name] + size_values[:6]

def split_descriptions(text):
    pattern = r'(?<=\d)(?=[가-힣]+\s*:|[A-Z]+\s*:)'
    return re.split(pattern, text)

converted_size_dic_list = []

for item in size_dic_list:
    new_item = {}
    for key, value in item.items():
        descriptions = split_descriptions(value[0])
        new_value = [parse_description(desc.strip()) for desc in descriptions]
        new_item[key] = new_value
    converted_size_dic_list.append(new_item)

print(converted_size_dic_list)


# 예외처리 추가








