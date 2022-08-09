from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import numpy as np
import pandas as pd
import time
import json
from bs4 import BeautifulSoup as bs
driver = webdriver.Firefox(executable_path='./geckodriver.exe')
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
        general_list = tex.split(";")
        general_list[0] = general_list[0].split("/")
        if len(general_list) == 2:
            general_list[1] = general_list[1].split(" ")
            for i in range(len(general_list[1])):
                general_list[1][i] = int(re.sub('\D', '', general_list[1][i]))
            q = list(zip(general_list[0], general_list[1]))
        id_list.append(q)
    actual = []
    for item in id_list:
        actual += item
    hier_index = pd.DataFrame(actual, columns=['General', 'id'])
    df = pd.DataFrame(np.zeros(len(actual)),columns=['score'])
    df = pd.concat([hier_index, df], axis=1)
    return df

def findFriends(html):
    rex = r'"text":".*\sfriends"'
    friends = re.findall(rex,html)
    if friends == []:
        return 0
    hell = re.findall(r'(\d+(?:\.\d+)?)', friends[0])
    if 'K' in friends[0]:
        return float(hell[0])*1000
    else:
        return float(hell[0])   
def findName(html):
    soup =bs(html, 'html.parser')
    name1=soup.title.get_text()
    name2 = name1.replace('(2)', "")
    name3 = name2.replace(' | Facebook', '')
    return name3
def findInfo(html):
    soup = bs(html, 'html.parser')
    test = soup.find_all('div', class_='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t d2edcug0 hpfvmrgz rj1gh0hx buofh1pr g5gj957u o8rfisnq p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt')
    array = []
    for thing in test:
        if "instagram" not in str(thing) and'twitter' not in str(thing) and 'facebook' not in thing.get_text():
            array.append(thing.get_text())
    array = np.array(array)
    array1 = np.unique(array)
    dict = {"Hometown":"", 'Current_town':"", "Job": []}
    if array1.size == 0:
        return dict
    for item in array1:
        if 'From' in item:
            dict["Hometown"] = item.split("From")[1]
        elif " in " in item and not "Studied" in item:
            dict["Current_town"] = item.split(' in ')[1]
        elif 'Works at ' in item or 'Worked at' in item:
            dict["Job"].append(item.split(' at ')[1])
        elif 'Studied ' not in item and 'Went' not in item and 'From' not in item and 'Lives' not in item and not 'https' in item and ' in ' not in item and "Pronounces" not in item:
            if "It's" not in item and "Widowed" not in item and "Joined" not in item and 'facebook' not in item and 'Divorced' not in item:
                if ' with ' not in item and 'In ' not in item and 'relationship' not in item and 'Married' not in item and "Followed" not in item and "Engaged" not in item and "Single" not in item:
                    dict["Job"].append(item)
    return dict
def pseudo_page_count(driver):
    for i in range(8):
        driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
        time.sleep(1)
    source_data = driver.page_source
    bs_data = bs(source_data, 'html.parser')
    posts = bs_data.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    return(len(posts))

def jobTest(row):
    for job in (row['Job']):
        if("Army" in str(job).lower()):
            return True
        else:
            return False

login(driver)
generalSearch(driver)
df = getDataFrame()
driver.close()
driver = webdriver.Firefox(executable_path='./geckodriver.exe')
login(driver)
count = 0
newdata = pd.DataFrame()
for idx, data in df.groupby(level='id'):
    array = []
    driver.get('https://www.facebook.com/profile.php?id=' + idx)
    html = driver.page_source
    friends = findFriends(html)
    info = findInfo(html)
    job = info['Job']
    current_town = info['Current_town']
    home_town = info['Hometown']
    name = findName(html)
    page_count = pseudo_page_count(driver)
    row = pd.DataFrame(data = np.array([[idx,name,job, current_town, home_town, page_count, friends]],dtype=object),columns=['id','Name','Job','Current_town', 'Home_town', 'Page_count', 'Friends'])
    if count%15 == 0 and count != 0:
        time.sleep(3)
    count +=1
    newdata = pd.concat([newdata, row])
driver.close()
newdata.set_index('id', inplace=True)
datatoexcel = pd.ExcelWriter('facebook.xlsx')
newdata.to_excel(datatoexcel)
datatoexcel.save()
data = pd.ExcelFile('facebook.xlsx')
newdata= data.parse('Sheet1')
newdata
newdata = pd.merge(df, newdata, left_on='id', right_on='id')
newdata.set_index('id', inplace=True)
