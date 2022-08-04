from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("headless")
driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=option)

def login(driver):
    with open("smith.txt", 'r') as f:
        account = (f.read()).split(",")
    driver.get("https://www.facebook.com/")
    elem = driver.find_element(By.XPATH, '//*[@id="email"]')
    elem.clear()
    elem.send_keys(account[0])
    passw = driver.find_element(By.XPATH,'//*[@id="pass"]')
    passw.send_keys(account[1])
    passw.send_keys(Keys.RETURN)
    time.sleep(5)
def general_search(driver):
    driver.get('https://www.facebook.com/search/people/?q=john%20W%3E%20Aarsen')
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
    source_data = driver.page_source
    bs_data = bs(source_data, 'html.parser')
    with open('text.html',"w", encoding="utf-8") as file:
                    source_data = driver.page_source
                    bs_data = bs(source_data, 'html.parser')
                    file.write(str(bs_data.prettify()))

login(driver)
general_search(driver)