import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

main_url = "https://www.zardins.com/product/list.html?cate_no=43"

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

name_list, img_list, link_list, size_dic_list = [], [], [], []

driver.get(url)
driver.implicitly_wait(time_to_wait=5)