
import math
import os
import io
import time
import urllib
import requests # request wysyłany do strony
import shutil   # to save it locally
import json
import gspread
import re   # Biblioteka do używania REGEX
import pandas as pd #Biblioteka tworzenia tabel i plików csv
#Biblioteka pozwalająca ominąć wyzwalanie serwisów anti-bot
import undetected_chromedriver as uc
    #Google drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
    #Biblioteka komend pydrive do obsługi google drive
from pygdrive3 import service
    #Poświadczenia użytkownika oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
    #Podstawowa biblioteka obsługująca kartę przeglądarki
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
    #Narzędzie do wykonywania skryptów selenium (używam do otwierania nowej karty)
from selenium.webdriver.common.action_chains import ActionChains
    #EC jako sprawdzenie czy dany element jest/da się liknąć/itp. itd.
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def manual_error_manager():
    print("Some error")
    input("Press Enter to continue...")
    input("Press Enter to continue...")

CHROMEDRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(CHROMEDRIVER_PATH)
#driver.get('https://warsawsneakerstore.com/air-trainer-1-sp-dh7338-300.html')


driver = uc.Chrome(use_subprocess=True)
driver.execute_script('return navigator.webdriver')
driver.get('https://warsawsneakerstore.com/air-trainer-1-sp-dh7338-300.html')
driver.execute_script('return navigator.webdriver')
#driver.get('https://distilnetworks.com')

'''
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
driver.get('https://warsawsneakerstore.com/air-trainer-1-sp-dh7338-300.html')
'''