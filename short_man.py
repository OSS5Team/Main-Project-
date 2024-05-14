import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

url = "https://smallman.co.kr/product/list.html?cate_no=5018"


chromedriver_autoinstaller.install()
driver = webdriver.Chrome()


name_list, img_list, link_list = [], [], []

driver.get(url)
driver.implicitly_wait(time_to_wait=5)
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")

sizes = soup.select(".sp-product-box")


for size in sizes:
  divs = size.find_all(attrs={'class': "sp-product-item-thumb-href"})
  for div in divs:

    link = div.attrs["href"]
    link_list.append("https://smallman.co.kr/" + link)

    imgs = div.find('img')
    
    img = imgs["src"]
    img_list.append(imgs)

    name = imgs["alt"]
    name_list.append(name)
    
