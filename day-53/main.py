from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import requests
import re
import os

chromedriver_path = os.environ.get('path')
URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64481581640625%2C%22east%22%3A-122.22184218359375%2C%22south%22%3A37.64356042534286%2C%22north%22%3A37.906788179891414%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}


class DataAutomation:

    def __init__(self):
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'lxml')
        self.links = []
        self.prices = []
        self.addresses = []

    def retrieve_listings(self):
        self.links = list(set([link.get('href') for link in self.soup.find_all(name='a', class_='list-card-link')]))
        self.prices = [price.getText()[:6] for price in self.soup.find_all(class_='list-card-price')]
        self.addresses = [address.getText() for address in self.soup.find_all(class_='list-card-addr')]
        for index, link in enumerate(self.links):
            if "http" not in link:
                self.links[index] = f"https://www.zillow.com{link}"

    def fill_form(self):
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        for index, address in enumerate(self.addresses):
            driver.get('https://forms.gle/NrtkajFeP9hiLNnu8')
            time.sleep(1)
            inputs = driver.find_elements_by_class_name('exportInput')
            submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
            inputs[0].send_keys(address)
            inputs[1].send_keys(self.prices[index])
            inputs[2].send_keys(self.links[index])
            submit.click()


data = DataAutomation()
data.retrieve_listings()
data.fill_form()
