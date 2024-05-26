import requests
from bs4 import BeautifulSoup

url = 'https://hisfit.co.kr/'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Example: Extract product names and prices
    products = soup.find_all('div', class_='item-cont')

    for product in products:
        name = product.find('div', class_='title').get_text(strip=True)
        price = product.find('div', class_='price').get_text(strip=True)
        print(f'Product Name: {name}, Price: {price}')
else:
    print('Failed to retrieve the webpage')

