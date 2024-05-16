import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

main_url = "https://www.byslim.com/category/top/6/"


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_dic_list = [], [], [], []

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

  td_tags = soup.find_all("td")
  for td in td_tags:
      if 'style' in td.attrs:
          if td.text.strip()[0] == "착":
              break 
          else: 
              size_list.append(td.text.strip())  
  save_size(name_list, size_list)
  return "complete getting size data"
              
def save_size(name_list, size_list):
  test_dic = {name_list[0]: None}
  temp_size_list = list()
  for i in size_list:
    if '(' in str(i):
      temp_size_list.append(size_list[size_list.index(i):size_list.index(i)+7])
  test_dic = {name_list[0]:temp_size_list}
  size_dic_list.append(test_dic)
      
print(get_list(main_url))
print(len(name_list))
print(len(img_list))
print(len(link_list))

for index in range(3):
   get_size(link_list[index], name_list)


print(size_dic_list)
   










