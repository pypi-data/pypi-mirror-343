import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = '/usr/bin/chromedriver'

# Set up Chrome options for Tor
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # Use Tor SOCKS5 proxy

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def main():
    parser = argparse.ArgumentParser(description='Web scraper using Selenium with Tor.')
    parser.add_argument('--url', required=True, help='The .onion URL to scrape')
    parser.add_argument('--output', default='output.txt', help='Output file (default: output.txt)')
    args = parser.parse_args()

    try:
        url = args.url
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        links = driver.find_elements(By.TAG_NAME, 'a')
        with open(args.output, 'w') as f:
            for link in links:
                href = link.get_attribute('href')
                if href:
                    print(href)
                    f.write(href + '\n')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
