import time
import csv
from datetime import datetime
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

#SET YOUR GOOGLE MEET SCHEDULE CSV FILE PATH HERE
meet_file_path = 'P:/autoMeet/meet_info.csv'

options = webdriver.ChromeOptions()

#PASTE THE PATH TO YOUR CHROME PROFILE FOLDER IN PLACE OF P:/autoMeet/User Data
options.add_argument("user-data-dir=P:/autoMeet/User Data")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

print("Opening Chrome")
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
driver.maximize_window()

# Function to ensure bitsmail is used for login
def ensure_bitsmail():
    joinCheck = driver.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac']")

    if(joinCheck.text == 'Ask to join'):
        switch_acc_button = driver.find_element_by_xpath("//a[@class='Kx3qp IOxzuf']")
        switch_acc_button.click()
        to_bitsmail = driver.find_elements_by_css_selector('.d2laFc .wLBAL')
        for email in to_bitsmail:
            if (email.text.find('hyderabad.bits-pilani.ac.in') != -1):
                email.click()
                break

# Function to disable mic and cam before joining
def disable_media():
    cam_mic = driver.find_elements_by_xpath("//div[@class='U26fgb JRY2Pb mUbCce kpROve uJNmj HNeRed QmxbVb']")
    for media in cam_mic:
        media.click();

# Function combining others to join google meet
def connect_to_meet(url, end_time):
    print("Opening Link now")
    driver.get(url)
    time.sleep(5)
    print("Ensuring bitsmail login")
    ensure_bitsmail()
    time.sleep(5)
    print("Disabling camera and mic")
    disable_media()

    print("Joining the meet!")
    join = driver.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac']")
    join.click();
    while True:
        time.sleep(15)
        time_now = int(datetime.now().strftime('%H%M'))
        if(time_now >= end_time):
            print("Time to end the meet.")
            time.sleep(3)
            driver.get("https://www.google.com")
            break

# Main driver code which reads the schedule, check for system time with meeting time, and then proceed to connect
with open(meet_file_path) as csvfile:
    print("Opening CSV File")
    data = csv.reader(csvfile, delimiter = ',')
    current_system_time = int(datetime.now().strftime('%H%M'))
    for meeting in data:
        print("Checking for link: "+meeting[2])
        start_time = int(meeting[0])
        end_time = int(meeting[1])
        if(start_time<=current_system_time and current_system_time<=end_time):
            print("It's time to connect to: "+meeting[2])
            url = meeting[2]
            connect_to_meet(url, end_time)
        elif(current_system_time < start_time):
            print("It's not time yet, waiting to connect to: "+meeting[2])
            time.sleep((start_time-current_system_time)*60)
            url = meeting[2]
            connect_to_meet(url, end_time)

driver.close()
