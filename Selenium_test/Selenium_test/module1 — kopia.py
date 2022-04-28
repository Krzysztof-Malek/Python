import os
import io
import time
import json
import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

###Zmienne do osbługi API sheets/drive
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('selenium-324620-5e93451f6152.json')

gc = gspread.authorize(credentials)

"""
gauth = GoogleAuth()
dc = GoogleDrive(gauth)

#file1 = dc.CreateFile({'title': 'Hello.txt'})
gfile = dc.CreateFile({'parents': [{'id': '1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz', name: 'fx.jpg'}]})
#gfile.SetContentFile('C:\\Users\\krzys\\Desktop\\ff\\arpex\\1.jpg')
gfile.SetContentFile('')
gfile.Upload()
file1.Upload() # Upload the file.
print('title: %s, id: %s' % (file1['title'], file1['id']))
"""

#wks = gc.open("Szablon Allegro").sheet1

###Otwarcie przeglądarki
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://b2b.arpex.com.pl/")

###Logowanie do konta użytkownika

    #Czekanie na pojawienie się okna do wpisania nazwy firmy
try:
    customerName = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "customerName-field"))
    )

    search = driver.find_element_by_id("customerName-field")
    search.send_keys("H MEGA TYCHY")

    #Wpisanie reszty danych logowania i zaznaczenie wymaganego checkboxa
    search = driver.find_element_by_id("userName-field")
    search.send_keys("Katarzyna Małek")
    search = driver.find_element_by_id("password-field")
    search.send_keys("arpex")
    search = driver.find_element_by_name("LoginConfirmation")
    search.click()
    time.sleep(3)
    button = driver.find_element_by_class_name("primary-action")
    button.click()

    time.sleep(1)
    driver.get("http://b2b.arpex.com.pl/items/11041?parent=10900")

except:
    print("Nie znalazlo pola logowania")
    time.sleep(5)
    driver.quit()

try:
    time.sleep(3)
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div/ul/li/a"))
    )

    button.click()

except:
    print("Nie znalazlo przedmiotu")
    time.sleep(5)
    driver.quit()



    #Zmienne do zapisywania zdjęcia (liczba oznaczająca nazwę i adresy)
count = 1
jpg = ".jpg"
folderAdres = "C:\\Users\\krzys\\Desktop\\ff\\arpex\\"

wasTried = 0;

try:
    available = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[3]/div/div/span[2]"))
    )

except:
    print("Nie znalazlo stanu magazynowego")
    time.sleep(5)
    driver.quit()

#time.sleep(4)

#pętla while aby na pewno wczytał się stan magazynowy -> można przerobić na try dla span[2]
while (wasTried < 2):
    if (driver.find_element_by_xpath("//div[3]/div/div/span[2]").text == 'jest'):
        print("111")
    
        wasTried = 2
        #howManyImg = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]")
        #if (howManyImg.text):
    
        time.sleep(2)
        driver.find_element_by_xpath("//app-slider/div/div").click()

        #Ustawienie domyślnej ilości zdjęć na 1 i sprawdzenie ilości zdjęć (patrząc po indexie 1 diva w karuzeli)
        imgCount = 1
        if(driver.find_element_by_class_name("swiper-slide-active")):
            if(driver.find_element_by_class_name("image-container").get_attribute('data-swiper-slide-index') == "0"):
                print("No siema")
                imgCount = 2
            elif(driver.find_element_by_class_name("image-container").get_attribute('data-swiper-slide-index') == "1"):
                imgCount = 3
            else:
                imgCount = 4

        for x in range (imgCount):
            img = driver.find_element_by_xpath("//div/div/div/div[3]/img")

            #Zapisanie całej ścieźki zapisu do jednej zmiennej i zinkrementowanie nazwy
            mergedImgName = folderAdres + str(count) + jpg
            count += 1

            #Zapisanie obrazu na dysku
            with open(mergedImgName, 'wb') as file:
                file.write(img.screenshot_as_png)


    else:
        print("000")
        if (wasTried == 1):
            driver.back()
        wasTried += 1
        time.sleep(5)

wasTried = 0


time.sleep(5)

#driver.quit()