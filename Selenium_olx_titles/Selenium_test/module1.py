import os
import io
import time
import urllib
import requests # to get image from the web
import shutil   # to save it locally
import json
import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from apiclient import discovery

from apiclient.http import MediaFileUpload
#from apiclient.http import MediaIoBaseDownload
from pygdrive3 import service
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError as HTTPError


from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/krzys/source/repos/Private/Klucze_do_aplikacji/selenium-324620-5e93451f6152.json')

gc = gspread.authorize(credentials)

#Otwarcie ścieżki dostępu do wybranego arkusza
wks = gc.open("Szablon Allegro").sheet1

gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#gauth.CommandLineAuth()
dc = GoogleDrive(gauth)

imagesList = []
folder_id = '1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz'

file_list = dc.ListFile({'q': "'1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz' in parents and trashed=false"}).GetList()
for file1 in file_list:
    imagesList.append(file1['id'])
    print('title: %s, id: %s' % (file1['title'], file1['id']))

imagesList.reverse()

cellNumber = 1
whichImgNow = 1
count = 50

for cellNumber in range (1, count+1):
    imgCell = "H" + str(cellNumber)
    howManyImg = wks.acell(imgCell).value

    imgSrcString = ''
    for j in range (1, int(howManyImg)+1):
        imgSrcString += 'https://drive.google.com/uc?id=' + imagesList[whichImgNow-1]
        whichImgNow += 1
        if (int(howManyImg) > 1 and int(howManyImg) != j):
            imgSrcString += '|'
    wks.update(imgCell, imgSrcString)
