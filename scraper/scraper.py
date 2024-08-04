from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
import sqlite3
from db.karta import Karta

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")

cookies = {
    'PHPSESSID': '5os2qocc94kb2lbgrscr6srngb',
    '_cfuvid': 'ssSeDVwP8Jk.JN8Y6Ol4m6ucR6CPLzBsY4yrpjx5f7Q-1722074177563-0.0.1.1-604800000	',
    '_ga': 'GA1.1.1437496798.1700832934',
    '_ga_G8GDQ4EM48': 'GS1.1.1703331270.4.0.1703331270.60.0.0',
    '_uetvid': '582011708ace11eeb0a3832f890ef2f0',
    '_vwo_ssm': '1',
    '_vwo_uuid': 'D0981BE1E635AAD15FDFB71848A9DC9C3',
    '_vwo_uuid_v2': 'DF3214716F6CBCD56121DA444A1E9DDA7',
    'cookie_settings': 'preferences%3D1%2Cstatistics%3D1%2Cmarketing%3D1'
}

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


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
        'availability': availability_number,
        'price': price,
    }
    
    return product


def scrape_data():

    karta = Karta()
    karta.create_table()

    for i in range(1,15):
        base_url = 'https://www.cardmarket.com/en/Pokemon/Products/Singles?idCategory=51&idExpansion=0&idRarity=0'
        url = f'{base_url}&site={i}'
        driver.get(url)
        
        time.sleep(2)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table_body = soup.find('div', class_='table-body')

        product_rows = table_body.find_all('div', id=re.compile(r'^productRow\d+'))

        products = [extract_product_data(row) for row in product_rows]

        for product in products:
            karta.insert_data(product['product_name'], product['availability'], product['price'], product['img_src'])
            print(f"Inserted: {product['product_name']}")

    driver.quit()
    
if __name__=="__main__":
    scrape_data()
