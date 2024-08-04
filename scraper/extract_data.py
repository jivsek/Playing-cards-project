from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


def extract_product_data(row):
    
    # Extract image url
    img_tag = row.find('span', class_='thumbnail-icon')
    img_url = None
    if img_tag:
        img_url = re.search(r'src="(.*?)"', img_tag['aria-label']).group(1)

    # Extract card name
    product_name_tag = row.find('div', {'class': 'col-10 col-md-8 px-2 flex-column align-items-start justify-content-center'})
    product_name = product_name_tag.find('a').text.strip() if product_name_tag else None
    
    # Extract availability number
    availability_tag = row.find('div', {'class': 'col-availability px-2'})
    availability_number = availability_tag.find('span', {'class': 'd-none d-md-inline'}).text.strip() if availability_tag else None

    # Extract price
    price_tag = row.find('div', {'class': 'col-price pe-sm-2'})
    price = price_tag.text.strip() if price_tag else None

    product = {
        'img_src': img_url,
        'product_name': product_name,
        'availability_number': availability_number,
        'price': price,
    }
    
    return product
