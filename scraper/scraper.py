from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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

driver.get("https://www.cardmarket.com/en/Pokemon/Products/Singles?idCategory=51&idExpansion=0&idRarity=0&sortBy=name_asc&perSite=20")

html_content = driver.page_source

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the div with class 'table-body'
table_body = soup.find('div', class_='table-body')

print(table_body)

for product in product_elements:
    title_element = product.find_element(By.CSS_SELECTOR, 'a')
    title = title_element.text
    print(title)

# Close the browser
driver.quit()



