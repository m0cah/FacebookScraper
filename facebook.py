# <---  Initial Imports --->
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import numpy as np
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import os
load_dotenv()
# <---  End of Initial Imports --->

# <--- Start of Functions --->
def login(driver):
    driver.get("https://www.facebook.com/")
<<<<<<< HEAD
    email = driver.find_element(By.XPATH, '//*[@id="email"]')
    sleep(1.5)
    email.send_keys(os.getenv('EMAIL'))
    password = driver.find_element(By.XPATH,'//*[@id="pass"]')
=======
    email = driver.find_element(By.ID, 'email')
    sleep(1.5)
    email.send_keys(os.getenv('EMAIL'))
    password = driver.find_element(By.ID,'pass')
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    sleep(1.5)
    password.send_keys(os.getenv('PASWD'))
    sleep(1.5)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button').click()
def generalNameList():
    x = pd.read_csv('names.csv')
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
        expression = '"profile":{"__typename":"User","__isNode":"User","id":"[0-9]*"'
        ids = re.findall(expression, textual_healing)
        x = np.array(ids)
        p = np.unique(x)
        gen = (general + "/")*len(p)
        p = " ".join(p)
        gen2 = gen + ";" + p
        master_list += str(gen2) + "\n"
        if count%15 == 0 and count != 0:
            sleep(20)
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
    df.set_index('id', inplace=True)
    return df
def getFriendCount(html):
    rex = r'"text":".*\sfriends"'
    friends = re.findall(rex, html)
    if friends == []:
        return 0
    hell = re.findall(r'(\d+(?:\.\d+)?)', friends[0])
    if 'K' in friends[0]:
        return float(hell[0])*1000
    else:
        return float(hell[0])   
<<<<<<< HEAD
def getName(html):
    soup =bs(html, 'html.parser')
    name1=soup.title.get_text()
    name2 = name1.replace('(2)', "")
    name3 = name2.replace(' | Facebook', '')
    return name3
=======
def getName(soup):
    return soup.find('span', {"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 embtmqzv h6olsfn3 mhxlubs3 p5u9llcw hnhda86s oo9gr5id hzawbc8m"}).get_text()
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    
def getIntro(soup):
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
def getPostCount(soup):
    posts = soup.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    return(len(posts))
def getBannerImageURL(soup):
    bannerImage = soup.find("img", {"data-imgperflogname" : "profileCoverPhoto"})
    if(bannerImage is not None and bannerImage.has_attr('src')):
        return bannerImage['src']
    else:
        return "No Banner"
def getProfilePictureURL(soup):
    q = soup.find('div',class_='b3onmgus e5nlhep0 ph5uu5jm ecm0bbzt spb7xbtv bkmhp75w emlxlaya s45kfl79 cwj9ozl2')
<<<<<<< HEAD
    image_url = ""
    if not isinstance(q, type(None)):
        r = q.find('image')
        rex = r'href=".*" '
        x = re.findall(rex,str(r))
        p = x[0]
        # removed = re.split('xlink:href=")
        almost_there=p.replace('href="', '')
        p = almost_there.replace('"', '')
        image_url = p.replace('amp;', '')
=======
    r = q.find('image')
    rex = r'href=".*" '
    x = re.findall(rex,str(r))
    p = x[0]
    # removed = re.split('xlink:href=")
    almost_there=p.replace('href="', '')
    p = almost_there.replace('"', '')
    image_url = p.replace('amp;', '')
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    return image_url
def getPostElements(soup):
    multiple=[]
    posts = soup.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')
    for post in posts:
<<<<<<< HEAD
        data = {}
=======
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
        date = post.find('a', class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')
        status = post.find('span', class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v b1v8xokw m9osqain')
        image = post.find('img')
        text = post.find('div', class_='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q')
        try:
            link = post.find('a', class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 datstx6m k4urcfbm')['href']
        except:
            link = ""
<<<<<<< HEAD
        data["link"]=link
=======
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
        try:
            text = text.get_text()
        except:
            text = ""
<<<<<<< HEAD
        data['text'] = text
        try:
            date= date.get_text()
        except:
            date=""
        data['date'] = date
        try:
            status = status.get_text()
        except:
            status = ""
        data['status'] = status
        try:
            image=image['src']
=======
        image=image['src']
        if type(status) == type(None):
            data = {'status':"", 'date':date.get_text()}
        else:
            data = {'status':status.get_text(), 'date': date.get_text(), 'text' : text, 'link':link}
        try:
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
            url = image.replace('amp;', '')
            data['image_url'] = url
        except:
            data['image_url'] = ""
        multiple.append(data)
    return multiple
<<<<<<< HEAD
def getFriendList(id,driver, friends):
    friendlist = []
    if friends > 0:
        driver.get("https://www.facebook.com/profile.php?id="+str(id)+"&sk=friends")
        for i in range(8):
            driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
            sleep(1.1)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        lister = soup.find('div', class_='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd')
        if not isinstance(lister, type(None)):
            friends = lister.find_all('div', class_='buofh1pr hv4rvrfc')
            for friend in friends:
                name = friend.find('span',class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id')
                link = friend.find('a')['href']
                name = name.get_text()
                data = {'name':name, 'link':link}
                friendlist.append(data)
=======
def getFriendList(driver):
    driver.get("https://www.facebook.com/profile.php?id="+str(id)+"&sk=friends")
    for i in range(8):
        driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
        sleep(1.1)
    html = driver.page_source
    friendlist = []
    soup = bs(html, 'html.parser')
    lister = soup.find('div', class_='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd')
    if not isinstance(lister, type(None)):
        friends = lister.find_all('div', class_='buofh1pr hv4rvrfc')
        for friend in friends:
            name = friend.find('span',class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id')
            link = friend.find('a')['href']
            name = name.get_text()
            data = {'name':name, 'link':link}
            friendlist.append(data)
    newdata.at[id,'Friend_Info'] = friendlist
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    return friendlist
def getPostStats(soup):
    posts = soup.find_all('div', {"class" : "stjgntxs ni8dbmo4 l82x9zwi uo3d90p7 h905i5nu monazrh9"})
    divElements = []
    for post in posts:
        try:
            divElements.append(post.find('div', {"class" : "bp9cbjyn m9osqain j83agx80 jq4qci2q bkfpd7mw a3bd9o3v kvgmc6g5 wkznzc2l oygrvhab dhix69tm jktsbyx5 rz4wbd8a osnr6wyh a8nywdso s1tcr66n"}))
        except:
            divElements.append(None)
    numCommentsList = []
    for commentsElements in divElements:
        try:
            commentElement = commentsElements.find('span',{"class": "d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain"})
            if("Comment" in commentElement.get_text()):
                commentText = commentElement.get_text()
            else:
                commentText = "0 Comments"
        except:
            commentText = "0 Comments"
        numCommentsList.append(commentText)
    numSharesList = []
    for shareElements in divElements:
        try:
            shareElement = shareElements.find('span',{"class": "d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain"})
            if("Share" in shareElement.get_text()):
                shareText = shareElement.get_text()
            else:
                shareText = "0 Shares"
        except:
            shareText = "0 Shares"
        numSharesList.append(shareText)
    numLikesList = []
    for likeElements in divElements:
        try:
            likeElement = likeElements.find('span',{"class": "gpro0wi8 cwj9ozl2 bzsjyuwj ja2t1vim"})
            likeText = likeElement.get_text() + " Likes"
        except:
            likeText = "0 Likes"
        numLikesList.append(likeText)
    return [numCommentsList, numLikesList, numSharesList]
def nameTest(id):
    global newdata
    general = newdata.at[id, 'General']
    name = newdata.at[id, 'Name']
    name = name.split(' ')
    same = False
    general = general.split(' ')
    if len(general) == len(name) and len(general)==3:
        if general[0].lower() == name[0].lower():
            if general[1][0].lower() == name[1][0].lower():
                if general[2].lower() == name[2].lower():
                    same = True
    elif len(general) == len(name) and len(general)==2:
        if general[0].lower() == name[0].lower():
            if general[1].lower() == name[1].lower():
                same = True
    elif len(general) == 3:
        if general[0].lower() == name[0].lower():
            if general[2].lower() == name[1].lower():
                same = True
    elif len(general)==4 and len(general)==len(name):
        if general[0].lower() == name[0].lower():
            if general[1][0].lower() == name[1][0].lower():
                if general[2].lower() == name[2].lower():
                    if general[3][0:2].lower() == name[3][0:2].lower():
                        same = True

    else:
        if general[0].lower() == name[0].lower():
            if general[1].lower() == name[-1].lower():
                same = True
    if same:
        newdata.at[id,'name_is_same'] = True
    return same
def jobTest(id):
    global newdata
    jobs = newdata.at[id,'Job']
    jobs =jobs[2:len(jobs)-2].split(',')
    if jobs ==[""]:
        newdata.at[id, 'in_army'] = True
        return True
    for job in jobs:
        if"army" in str(job).lower() or 'general' in str(job).lower():
            newdata.at[id, 'in_army'] = True
            return True
    return False
def postTest(id):
    global newdata
    count = newdata.at[id, 'Page_count']
    if count < 5:
        newdata.at[id, 'post_check'] = True
        return True
    else:
        return False
def friendTest(id):
    global newdata
    friends = newdata.at[id, 'Friends']
    if friends < 15:
        newdata.at[id, 'friend_check'] = True
        return True
    else:
        return False
def scoreCalc(idx,checks):
    global newdata
    count =0
    for check in checks:
        if check:
            count+=1
    if count == 1:
        newdata.at[idx, 'score'] = 15
    if count == 2:
        newdata.at[idx, 'score'] = 50
    if count == 3:
        newdata.at[idx, 'score'] = 75
    if count == 4:
        newdata.at[idx, 'score'] = 100
def scroll(driver):
<<<<<<< HEAD
    SCROLL_PAUSE_TIME = 1.2
=======
    SCROLL_PAUSE_TIME = 1
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
def run():
<<<<<<< HEAD
    driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    login(driver)
    count = 0
    df = getDataFrame()
=======
    count = 0
    df = getDataFrame()
    df.set_index('id', inplace=True)
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    newdata = pd.DataFrame()
    for idx in df.index:
        array = []
        driver.get('https://www.facebook.com/profile.php?id=' + str(idx))
        scroll(driver)
        html = driver.page_source
        soup = bs(html, 'html.parser')
<<<<<<< HEAD
        friends = getFriendCount(html)
        info = getIntro(soup)
        job = info['Job']
        current_town = info['Current_town']
        home_town = info['Hometown']
        name = getName(html)
        page_count = getPostCount(soup)
        bannerImageURL = getBannerImageURL(soup)
        profilePictureURL = getProfilePictureURL(soup)
        postStats = getPostStats(soup)
        postelements = getPostElements(soup)
        commentsPerPost = postStats[0]
        likesPerPost = postStats[1]
        sharesPerPost = postStats[2]
        friendList = getFriendList(idx,driver,friends)
        row = pd.DataFrame(data = np.array([[
            idx,
            name,
            job, 
            current_town, 
            home_town, 
            page_count, 
            friends, 
            bannerImageURL, 
            profilePictureURL, 
            friendList, 
            commentsPerPost, 
            likesPerPost, 
            sharesPerPost,
            postelements]
            ],dtype=object),
            columns=['id','Name','Job','Current_town', 'Home_town', 'Page_count', 'Number of Friends', 
            'Banner URL', 'Profile URL', 'Friends List', 'Comments', 'Likes', 'Shares', 'Post Elements'])
        if count%10 == 0 and count != 0:
            sleep(15)
=======
        friends = getFriendCount(soup)
        info = getIntro(html)
        job = info['Job']
        current_town = info['Current_town']
        home_town = info['Hometown']
        name = getName(soup)
        page_count = getPostCount(driver)
        bannerImageURL = getBannerImageURL(soup)
        profilePictureURL = getProfilePictureURL(soup)
        friendList = getFriendList(driver)
        commentsPerPost = getPostStats()[0]
        likesPerPost = getPostStats()[1]
        sharesPerPost = getPostStats()[2]
        row = pd.DataFrame(data = np.array([[idx,name,job, current_town, home_town, page_count, friends, bannerImageURL, profilePictureURL, friendList, commentsPerPost, likesPerPost, sharesPerPost]],dtype=object),columns=['id','Name','Job','Current_town', 'Home_town', 'Page_count', 'Number of Friends', 'Banner URL', 'Profile URL', 'Friends List', 'Comments', 'Likes', 'Shares'])
        if count%15 == 0 and count != 0:
            sleep(3)
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
        count +=1
        newdata = pd.concat([newdata, row])
    driver.close()
    newdata.set_index('id', inplace=True)
<<<<<<< HEAD
    datatoexcel = pd.ExcelWriter('facebook.xlsx')
    newdata.to_excel(datatoexcel)
    datatoexcel.save()
=======
    # datatoexcel = pd.ExcelWriter('facebook.xlsx')
    # newdata.to_excel(datatoexcel)
    # datatoexcel.save()
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
    newdata
# <---  End of Functions --->


# <--- Start of Main --->
<<<<<<< HEAD
# driver = webdriver.Firefox(executable_path='./geckodriver.exe')
# login(driver)
# generalSearch(driver)
run()
=======
driver = webdriver.Firefox(executable_path='./geckodriver')
login(driver)
generalSearch(driver)
soup = bs(html, 'html.parser')
>>>>>>> 42e9bbf0ebea384ae1d25223a13170cef8062c88
# <---  End of Main --->


# <---   --->

# <---   --->


# <---   --->

# <---   --->


# <---   --->

# <---   --->


# <---   --->

# <---   --->


# <---   --->

# <---   --->


# <---   --->

# <---   --->

