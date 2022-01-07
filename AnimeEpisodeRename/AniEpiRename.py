import requests
import os
from bs4 import BeautifulSoup

####################### FILL OPTIONS HERE #######################

#necessary
animeName='One Piece'
seasonNumber=1

#just google search your 'anime name + anidb' on google, go to the anime page on anidb website
#and fill the id number at the end of the link, for example if you search one piece
#the link is https://anidb.net/anime/69 hence the anidb_id would be 69
anidb_id=69

animeName = input("What is the anime name?")
seasonNumber = input("What is the anime season?")
directory = input("Enter the complete path to files: ")
anidb_id = input("Go to anidb.net, search your anime with season, and enter the anidb id of it: ")

#optional
groupName=''
#################################################################
os.chdir(directory)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
url = 'https://anidb.net/anime/'+str(anidb_id)
r=requests.get(url, headers=headers)
soup=BeautifulSoup(r.text,'html.parser')
tableRows=soup.findAll('tr',attrs={"itemprop":"episode"})
print("Filenames fetched.")
#################################################################
def onlyFiles(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and '.mkv' in file:
            yield file
#################################################################
count=0
for row, filename in zip(tableRows, onlyFiles('.')):
    epiNumber = row.find('abbr',attrs={"itemprop":"episodeNumber"}).text.strip()
    title = row.find('label').text.strip()

    #You can tweak this string to change the format in which the files are renamed, it's intuitive.
    #By defualt it renames like: One Piece - S01E01 - Im Luffy! The Man Whos Gonna Be King of the Pirates!.mkv
    newFileName = animeName+" - S"+str(seasonNumber).zfill(2)+"E"+epiNumber.zfill(2)+" - "+title+".mkv"

    chars = "\\`\'\"/*<>?|:"
    for c in chars:
        if c in newFileName:
            newFileName = newFileName.replace(c, "")

    if '.mkv' in filename:
        count+=1
        os.rename(filename, newFileName)
        print(filename + '  ==>  ' + newFileName)
        print('------------------------------------------------------------------------------')
print('------------------------------------------------------------------------------')
print(str(count)+" files renamed.")