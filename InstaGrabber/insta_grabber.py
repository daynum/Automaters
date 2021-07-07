#media/?size=l
import os
import time
import re
import requests
import shutil
from selenium import webdriver

username=input("Give me the Instagram profile username: ")
profile_link = 'https://www.instagram.com/'+username+'/'

#SET YOUR CHROMEDRIVER PATH HERE
driver_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=P:/autoMeet/User Data")
#options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

 #grabbing all picture links
driver.get(profile_link)
time.sleep(3)
height=1
prev_height=0
while prev_height < height:
    prev_height = driver.execute_script("return document.body.scrollHeight;")
    images = driver.find_elements_by_tag_name('a')
    url_list=[]
    for image in images:
        img_link = image.get_attribute("href")
        if '/p/' in img_link and img_link not in url_list:
            url_list.append(img_link+'media/?size=l') 
        else:
            continue
    #scroll and update height
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    height=driver.execute_script("return document.body.scrollHeight;")

print("Link fetching complete, downloading images...")
os.mkdir(username)
os.chdir(username)
for url in url_list:
    driver.get(url)
    time.sleep(2)
    url=driver.current_url
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))', url)
    if not filename:
        print("Regex didn't match with the url: {}".format(url))
        continue
    with open(filename.group(1), 'wb') as f:
        if 'http' not in url:
            url = '{}{}'.format(profile_link, url)
        response = requests.get(url)
        f.write(response.content)
print("Images downloaded successfully")
#time.sleep(5)
driver.quit()