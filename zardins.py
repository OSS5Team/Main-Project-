import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

main_url = "https://www.zardins.com/product/list.html?cate_no=43"

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_dic_list, size_list, size_list = [], [], [], [], []
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
  td_tags = soup.find_all("td")
  for td in td_tags:
    if 'style' in td.attrs:
      if td.text.strip()[0] == "모델":
        break 
      else:
        size_list.append(td.text.strip())  
  return "complete getting size data"



test_dic = {name_list[0]: None}
temp_size_list = list()
for i in size_list:
  if '(' in str(i):
    temp_size_list.append(size_list[size_list.index(i):size_list.index(i)+7])
test_dic = {name_list[0]:temp_size_list}
size_dic_list.append(test_dic)