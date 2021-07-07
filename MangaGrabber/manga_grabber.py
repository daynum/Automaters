import os
import time
import re
import requests
import shutil
from selenium import webdriver
import feedparser

#SET YOUR CHROMEDRIVER PATH HERE
driver_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

rss=input("Give me the mangasee rss link for your manga: ")
rss_dict = feedparser.parse(rss)
for chapter in rss_dict.entries:
    title = chapter.id
    head, sep, tail = chapter.link.partition('-page-')
    site = head+'.html'
    if os.path.isfile(title+'.cbz'):
        continue
    print("Fetching "+title+".")
    driver.get(site)
    time.sleep(5)
    #https://mangasee123.com/rss/Solo-Leveling.xml
    images = driver.find_elements_by_tag_name('img')
    url_list=[]
    for image in images:
        img_link = image.get_attribute("src")
        if 'manga' in img_link and img_link not in url_list:
            url_list.append(img_link) 
        else:
            continue

    print("Link fetching complete, downloading images...")
    os.mkdir(title)
    os.chdir(title)
    for url in url_list:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            #print("Regex didn't match with the url: {}".format(url))
            continue
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)
    print("Images downloaded successfully")
    print("Repacking into comic format")
    os.chdir("..")
    shutil.make_archive(title, 'zip', title)
    os.rename(title+'.zip',title+'.cbz')
    shutil.rmtree(title)
    #time.sleep(5)
driver.quit()