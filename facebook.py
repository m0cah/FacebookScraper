from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import numpy as np
import pandas as pd
import time
import json
access_token = 'EAAQSkouZCNP0BACuqUylUQ9LWAYgt97HirZAZBRxoBaRXPRd6e5p1tiswMeSncA2sIacFbDTG1v9mf8yCw6oC6lWVfiW6rEzIfdP24zPeF9wF1N4gTDk9RgM5m4q7PVNIIZCPNMxrbGDcIlLOYjkzTnDZBqvMpJjSqIkyBrR6vZAEe0pR3FuCp'
driver = webdriver.Firefox(executable_path='C:/Users/micah/geckodriver-v0.31.0-win64/geckodriver.exe')
def login(driver):
    with open("smith.txt", 'r') as f:
        account = (f.read()).split(",")
    driver.get("https://www.facebook.com/")
    elem = driver.find_element(By.XPATH, '//*[@id="email"]')
    elem.clear()
    elem.send_keys(account[0])
    passw = driver.find_element(By.XPATH,'//*[@id="pass"]')
    passw.send_keys(account[1])
    login = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
    login.click()
def generalNameList():
    #change to general once you find out what is going on
    x = pd.read_csv('C:/Users/micah/DigitalImposterProject/FaceBook_stuff/names.csv')
    return x['Generals'].to_list()
def nameToLink(name):
    return name.replace(" ", "%20")
def generalSearch(driver):
    generals = generalNameList()
    master_list = ""
    count = 0
    for general in generals:
        # elem = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/label/input')
        # elem.send_keys(general)
        driver.get("https://www.facebook.com/search/people/?q=" + nameToLink(general))
        textual_healing = driver.page_source
        expression = '"id":"[0-9]*"'
        ids = re.findall(expression, textual_healing)
        x = np.array(ids)
        p = np.unique(x)
        gen = (general + "/")*len(p)
        p = " ".join(p)
        gen2 = gen + "," + p
        master_list += str(gen2) + "\n"
        if count%15 == 0 and count != 0:
            time.sleep(10)
        count +=1
    driver.close()
    with open('general_ids.txt', 'w') as f:
        f.write(str(master_list))

def getDataFrame():
    q = open('general_ids.txt', 'r')
    text = q.read()
    text = text.split("\n")
    id_list= []
    for tex in text:
        general_list = tex.split(",")
        general_list[0] = general_list[0].split("/")
        if len(general_list) == 2:
            general_list[1] = general_list[1].split(" ")
            for i in range(len(general_list[1])):
                general_list[1][i] = re.sub('\D', '', general_list[1][i])
            q = list(zip(general_list[0], general_list[1]))
        id_list.append(q)
    actual = []
    for item in id_list:
        actual += item
    hier_index = pd.MultiIndex.from_tuples(actual)
    df = pd.DataFrame(np.zeros(len(actual)), index=hier_index, columns=['score'])
    df.index.names = ['general', 'id']
    return df

login(driver)
generalSearch(driver)
df = getDataFrame()
df.info()
