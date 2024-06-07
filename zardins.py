import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

main_url = "https://www.zardins.com/product/list.html?cate_no=43"

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_dic_list, size_list, size_list = [], [], [], [], []

driver.get(url)
driver.implicitly_wait(time_to_wait=5)
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")

td_tags = soup.find_all("td")
for td in td_tags:
  if 'style' in td.attrs:
    if td.text.strip()[0] == "모델":
      break 
    else:
      size_list.append(td.text.strip())  

test_dic = {name_list[0]: None}
 temp_size_list = list()