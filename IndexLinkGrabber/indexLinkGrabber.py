import time
import clipboard
from selenium import webdriver

r"""
1. Install Selenium library for python.

2. Download chromedriver software and note down it's location.

3. Copy your default chrome profile to some other directory and note down it's location.
   The chrome profile path is generally located at:
   C:\Users\<username>\AppData\Local\Google\Chrome\User Data\
   copy the "User Data" folder and paste it somewhere else, and copy this other location.

4. Type out your schedule in a CSV file and note down it's path. Start time and End time should be in 24h format,
   like for 04:33 PM you write 1633. For 09:05 AM write 0905.
    THE FORMAT OF CSV FILE SHOULD BE :
    STARTTIME,ENDTIME,LINK
    STARTTIME,ENDTIME,LINK
    STARTTIME,ENDTIME,LINK
"""
#SET YOUR CHROMEDRIVER PATH HERE
driver_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'

options = webdriver.ChromeOptions()

#PASTE THE PATH TO YOUR CHROME PROFILE FOLDER IN PLACE OF P:/autoMeet/User Data
options.add_argument("user-data-dir=P:/autoMeet/User Data")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

index_link = input("Enter the path to index folder: ")
filename = input("Enter file name: ")
print("Opening Chrome")
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
driver.maximize_window()
data=""
file = open("C:/Users/Dinank/Desktop/"+filename+".txt","a")

def getFileLinks(link):
    driver.get(link)
    time.sleep(30)
    fileLinks = driver.find_elements_by_class_name("fa-copy")
    for file_link in fileLinks:
        file_link.click()
        time.sleep(10)
        data = clipboard.paste()
        data+="\n"
        file.write(data)
getFileLinks(index_link)
driver.close()

