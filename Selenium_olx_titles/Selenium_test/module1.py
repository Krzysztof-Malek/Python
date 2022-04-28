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

credentials = ServiceAccountCredentials.from_json_keyfile_name('selenium-324620-5e93451f6152.json')

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


"""
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'selenium-324620-5e93451f6152.json'
APPLICATION_NAME = 'Test'

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drivedrive_service.filrs().list(
        pageSize=size,fields = 'nextPageToken, files(id, name)"').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1}'.format(item['name'], item['id']))
listFiles(100)
"""

"""
CLIENT_SECRET_FILE = 'selenium-324620-5e93451f6152.json'
API_NAME = 'Test'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('selenium-324620-5e93451f6152.json', 'Test', 'v3', SCOPES)

service = build('drive', 'v3', credentials=creds)
#service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz'

query = f"parent ='{folder_id}'"

response = service.files().list(q=query).execute()
files = response.get('files')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = response = service.files().list(q=query).execute()
    files.extend(response.get('files'))
    nextPageToken = response.get('nextPageToken')

df = pd.DataFrame('files')
print(df)

"""

"""
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://b2b.arpex.com.pl/")

###Logowanie do konta użytkownika

    #Czekanie na pojawienie się okna do wpisania nazwy firmy

driver.execute_script('''window.open("http://bings.com","_blank");''')
driver.switch_to.window(driver.window_handles[0])
driver.close()
driver.switch_to.window(driver.window_handles[1])

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('selenium-324620-5e93451f6152.json')

gc = gspread.authorize(credentials)

wks = gc.open("Szablon Allegro").sheet1

print(wks.get_all_records())

whichCell = 5
cellName = "H" + str(whichCell)
wks.update(cellName, "442323423432") #Dodaje w nowym wierszu

"""

"""
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://drive.google.com/drive/u/0/folders/1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz")
#uploadElement = driver.find_element(By.XPATH, "//button/div[2]").click()
print("g")
whichImg = 2;
imgName = str(whichImg) + ".jfif"
imgXpath = "//c-wiz[" + str(whichImg) + "]/div"
#dataId = driver.find_element_by_xpath("//c-wiz[2]/div").get_attribute('data-id')

if(whichImg == 1):
    dataId = driver.find_element_by_xpath("//c-wiz/div").get_attribute('data-id')
else:
    dataId = driver.find_element_by_xpath(imgXpath).get_attribute('data-id')

print("g")
driver.execute_script("Window.open()")
driver.switch_to.window(self.driver.window_handles[1])
driver.get("https://docs.google.com/spreadsheets/d/1C26gOmvaEUXxxdyGuf3LS2NN9kWgn00RDJWtNU641pE/edit#gid=124384060")
cell = driver.find_element_by_xpath()
"""


#driver.find_element_by_css_selector("body").sendKeys(Keys.CONTROL + "t")

"""
driver.get("http://demo.guru99.com/test/upload/")
driver.set_window_size(1536, 864)
uploadElement = driver.find_element(By.ID, "uploadfile_0")
uploadElement.send_keys("C:\\Users\\krzys\\Downloads\\temp.jfif")
driver.find_element(By.ID, "terms").click()
driver.find_element(By.NAME, "send").click()
"""


"""
executor_url = driver.command_executor._url
session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver

bro = attach_to_session('http://127.0.0.1:59047', '9bce91b7f7146881712f3a3d21f98fc6')
bro.get('http://ya.ru/')


driver.get("https://allegro.pl/offer/11103032881/restore")
driver.set_window_size(1536, 864)
driver.find_element(By.CSS_SELECTOR, ".icon-upload > .iohzf").click()
driver.find_element(By.CSS_SELECTOR, ".dropzone > input").send_keys("C:\\fakepath\\temp.jfif")
driver.find_element(By.CSS_SELECTOR, ".icon-upload").click()
driver.find_element(By.CSS_SELECTOR, "input:nth-child(3)").send_keys("C:\\fakepath\\2.jfif")
element = driver.find_element(By.CSS_SELECTOR, ".icon-upload")
actions = ActionChains(driver)
actions.move_to_element(element).perform()
driver.find_element(By.CSS_SELECTOR, ".icon-upload").click()
driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").send_keys("C:\\fakepath\\1.jfif")
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
actions.move_to_element(element, 0, 0).perform()
#driver.close()
"""





"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://olx.pl/")

print(driver.title)
#driver.close()  #close tab

search = driver.find_element_by_id("headerSearch")
search.send_keys("auto")
search.send_keys(Keys.RETURN)


try:
    offers_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "offers_table"))
    )
    
    wraps = offers_table.find_elements_by_class_name("offer-wrapper")
    for x in wraps:
        title = x.find_element_by_tag_name("strong")
        print(title.text)

finally:
    driver.quit()


#wrap = driver.find_element_by_class_name("wrap") 

#print(driver.page_source) #print all source of page

time.sleep(5)

driver.quit()   #close Chrome
"""