# from selenium import webdriver, common
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
#
#
# s = Service(r'C:\Users\ASER\Documents\GitHub\pars_project_vfat\Chrom\chromedriver.exe')
# driver = webdriver.Chrome(service=s)

url = 'https://kanaria.rmrk.app/catalogue?symbol=YLTD21&page=1&priceMax=.75&sortBy=price'
# driver.get(url)
# chek = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div').text
# print(chek)

import bs4
import requests
from bs4 import BeautifulSoup
data = requests.get(url).text

if 'Sorry! There are no collectibles matching your search' in data:
    print('yes')
else:
    print('no')


