"""
Notatki deweloperskie

Błędy:
    Usprawnić dodawanie linków w 2 części programu z powodu tego że lista może posiadać max 300 elementów

Możliwe usprawnienia:
    Można zrobić więcej sprawdzeń czy pewne elementy pojawiają się na stronie/czy można w nie kliknąć zamiast czekania kilku sekund
"""
    #Polskie znaki
from __future__ import unicode_literals
import codecs

import math
import os
import io
import time
import urllib
import requests # to get image from the web
import shutil   # to save it locally
import json
import gspread
import re   # Biblioteka do używania REGEX

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

#Funkcja aby ręcznie rozwiązać problem i nie przerywać całego programu - nie uruchamiać od nowa cały czas
def manual_error_manager():
    print("Some error")
    input("Press Enter to continue...")
    input("Press Enter to continue...")

###Zmienne do osbługi API sheets/drive
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/krzys/source/repos/Private/Klucze_do_aplikacji/selenium-324620-5e93451f6152.json')

gc = gspread.authorize(credentials)

#Otwarcie ścieżki dostępu do wybranego arkusza
wks = gc.open_by_key('1EsRk_dSHR074QVpktVUsl2E7yymoeQzjUUZW2XYvDFk').worksheet("Arkusz2")
gauth = GoogleAuth()
dc = GoogleDrive(gauth)

#Wzięcie haseł z pliku
pass_file = codecs.open("C:/Users/krzys/source/repos/Private/Klucze_do_aplikacji/pass_arpex.txt", 'r', 'utf-8')
Lines = pass_file.readlines()

customer_name = Lines[0].strip()
user_name = Lines[1].strip()
password = Lines[2].strip()



    #Jeżeli chcemy tylko dodać linki w kolumnie zdjęcia to if(0):
if(0):
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
        search.send_keys(customer_name)

        #Wpisanie reszty danych logowania i zaznaczenie wymaganego checkboxa
        search = driver.find_element_by_id("userName-field")
        search.send_keys(user_name)
        search = driver.find_element_by_id("password-field")
        search.send_keys(password)
        search = driver.find_element_by_name("LoginConfirmation")
        search.click()
        time.sleep(3)
        button = driver.find_element_by_class_name("primary-action")
        button.click()

        time.sleep(1)
        #driver.get("http://b2b.arpex.com.pl/items/10900?parent=0")     #główna strona
        driver.get("http://b2b.arpex.com.pl/items/10922?parent=10901")  #świąteczna strona

    except:
        print("Nie znalazlo pola logowania")
        time.sleep(5)
        driver.quit()

    ###Zmienne do zapisywania zdjęcia i numer wiersza excela (liczba oznaczająca nazwę i adresy)
        #Od której strony zacząć - default 1
    howManyPagesToSkip = 1 #było 18
        #Od którego wiersza zacząć wpisywanie do excela - default 1
    cellNumber = 1 #było 758
        #Numerowanie zdjęć - default 1 / bądź manualne sprawdzenie numerowania zdjęć w folderze
    count = 1 #było 1449
        #Od którego przedmiotu ma zacząć - default 1
    item = 1 #było 17

        #Stałe tekstowe
    jpg = ".jpg"
        #gdzie zapisać pobrane zdjęcia
    folderAdres = "C:\\Users\\krzys\\Desktop\\ff\\arpex_christmas\\" #było "C:\\Users\\krzys\\Desktop\\ff\\arpex\\"

    for p in  range (howManyPagesToSkip):
        time.sleep(5)
        #Przesunięcie strony dna koniec (aby wczytać całą stronę, w tym przycisk następnej strony)
        viewElement = driver.find_element_by_class_name("app-footer")
        actions = ActionChains(driver)
        actions.move_to_element(viewElement).perform()

        #Pobranie całkowitej ilości stron z artykułami
        howManyPages = driver.find_element_by_xpath("//app-pager/div/input").get_attribute("max")

            #Pominięcie stron
        if (p < howManyPagesToSkip-1):
            driver.find_element_by_xpath("//app-pager/div/button[2]/i").click()
        else:
            time.sleep(2)



    #Petla dla wszystkich stron
    for p in range (0, int(howManyPages)+1):

        #Zliczenie ofert na stronie i wykonanie pętli tyle samo razy (użyte find_elements zamiast element)
        time.sleep(5)
        offersCount = len(driver.find_elements_by_class_name('list-item'))

        #Przesunięcie strony dna koniec (aby wczytać całą stronę - przycisk następnej strony)
        viewElement = driver.find_element_by_class_name("app-footer")
        actions = ActionChains(driver)
        actions.move_to_element(viewElement).perform()

        #Sprawdzenie czy istnieje następna strona - czy przycisk da się kliknąć
        isNextPage = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//app-pager/div/button[2]/i"))
        )

        #Pętla dla wszystkich ofert na stronie
        for i in range (item, offersCount+1):

            itemXpath = "//div/ul/li[" + str(i) + "]/a"

            #Przesunięcie strony do wybranego przedmiotu
            time.sleep(2)
            viewElement = driver.find_element_by_xpath(itemXpath)
            actions = ActionChains(driver)
            actions.move_to_element(viewElement).perform()

            #Otwarcie nowej karty z przedmiotem
            itemLink = driver.find_element_by_xpath(itemXpath).get_attribute('href')
            itemScript = "window.open(\"" + itemLink + "\",\"_blank\");"
            driver.execute_script(itemScript)
            driver.switch_to.window(driver.window_handles[1])

            #Sprawdzenie wyświetlenia stanu magazynowego przedmiotu
            time.sleep(4)
            try:
                available = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[3]/div/div/span[2]"))
                )

            except:
                print("Nie znalazlo stanu magazynowego")
                manual_error_manager()

            #time.sleep(4)

            #pętla while aby na pewno wczytał się stan magazynowy -> można przerobić na try dla span[2]
            #driver.find_element_by_xpath("//div[3]/div/div/span[2]")
            if (available.text == 'jest'):
    
                wasTried = 2
                #howManyImg = driver.find_element_by_xpath("//div[2]/div/div/div/div[3]")
                #if (howManyImg.text):
    
                #EAN i paremetry produktu
                try:
                    price = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[2]/div[2]/span"))
                    )
                    title = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//h1"))
                    )


                except:
                    print("Nie znalazlo opisu")
                    manual_error_manager()

                #Sprawdzenie który <p> to EAN - nie ma swojego indentyfikatora i zmienia się ilosć informacji o produkcie
                try:
                    eanPattern = re.compile("^[0-9]+$")
                    ean = driver.find_element_by_xpath("//p[2]").text
                    if not(eanPattern.match(ean)):
                        ean = driver.find_element_by_xpath("//p[4]").text
                    if not(eanPattern.match(ean)):
                        ean = driver.find_element_by_xpath("//p[6]").text
                except:
                    print("Nie znalazło EAN")
                    manual_error_manager()

            


                title = driver.find_element_by_xpath("//h1").text
                if( len(driver.find_elements_by_xpath("//div[7]/div"))):
                    description = driver.find_element_by_xpath("//div[7]/div").text
                    description = description.replace("\n", " ")
                else:
                    description = title
                price = driver.find_element_by_xpath("//div[2]/div[2]/span").text

                eanCell = "A" + str(cellNumber)
                titleCell = "G" + str(cellNumber)
                descriptionCell = "I" + str(cellNumber)
                priceCell = "F" + str(cellNumber)
                howManyCell = "E" + str(cellNumber)
                signatureCell = "D" + str(cellNumber)
                imgCell = "H" + str(cellNumber)

                wks.update(eanCell, ean)
                wks.update(titleCell, title)
                wks.update(descriptionCell, description)
                wks.update(priceCell, price)
                wks.update(howManyCell, "100")
                wks.update(signatureCell, "Arpex")

                cellNumber += 1

                #time.sleep(2)                   #czy to jest potrzebne???
                try:
                    #Powiększenie zdjęcia
                    driver.find_element_by_xpath("//app-slider/div/div").click()

                    #Ustawienie domyślnej ilości zdjęć na 1 i sprawdzenie ilości zdjęć (patrząc po indexie 1 diva w karuzeli)
                    imgCount = 1
                        #Sprawdzenie czy istnieje prawy przycisk karuzeli (istnieje przy więcej niż 1 zdjęciu)
                    element = driver.find_elements_by_class_name("swiper-slide-active")
                    if (element):
                        if(driver.find_element_by_class_name("image-container").get_attribute('data-swiper-slide-index') == "0"):
                            imgCount = 2
                        elif(driver.find_element_by_class_name("image-container").get_attribute('data-swiper-slide-index') == "1"):
                            imgCount = 3
                        else:
                            imgCount = 4

                    wks.update(imgCell, imgCount)

                except:
                    wks.update(imgCell, "0")
                    imgCount = 0

                #Pętla otwierająca nową karte i zapisująca zdjęcia (prntscrn)
                for x in range (imgCount):
                    imgXpath = "//div/div/div/div[" + str(x+1) + "]/img"
                    imgSrc = driver.find_element_by_xpath(imgXpath).get_attribute("src")
                        #Zapisanie skryptu i wykonanie go - otwarcie nowej karty z samym zdjęciem
                    imgStr = "window.open(\"" + imgSrc + "\",\"_blank\");"
                    driver.execute_script(imgStr)

                    #Zapisanie całej ścieźki zapisu do jednej zmiennej
                    mergedImgName = folderAdres + str(count) + jpg

                    #Zapisanie obrazu na dysku
                    driver.switch_to.window(driver.window_handles[2])
                    img = driver.find_element_by_xpath("//img")
                    with open(mergedImgName, 'wb') as file:
                        file.write(img.screenshot_as_png)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
        
                    #ziinkrementowanie nazwy zdjęcia i przesuniecie karuzeli na następne zdjęcie
                    count += 1
                    try:
                        if (element):
                            driver.find_element_by_xpath("//div[2]/div/div/div[2]").click() ##Źle pobrało ilość zdjęć z paczki balonów mix kolorów na stronie 6
                    except:
                        print("Żle pobrało zdjęcia - najpewniej tylko 1")
                        imgCount = 1
                        wks.update(imgCell, imgCount)
                        manual_error_manager();
                        break;


                driver.back()
    

            else:
                print("000")
                driver.back()
                wasTried = 1
                time.sleep(5)

            wasTried = 0

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        if (isNextPage):
            driver.find_element_by_xpath("//app-pager/div/button[2]/i").click()


    input("Press Enter to continue...")
    input("Press Enter to continue...")
    input("Press Enter to continue...")
    input("Press Enter to continue...")

##################
##################
##################
##################
##################
######### Sekcja z wstawianiem linku do pobierania zdjęć do excela
##################
##################
##################
##################

imagesList = []
#id folderu ze zdjęciami
folder_id =  '1NFnQhiRhumKZIU8y3-vbMJrMr1kdnxDY' #'1x1QTYvRm1CTp9ZsdsEdzyuWc8suJ2uBE'
string_folder_id = "'{}' in parents and trashed=false".format(folder_id)

    #Numer wiersza od którego zaczyna - default 1
cellNumber = 60 #692

    #Nazwa zdjęcia od którego zaczyna - default '1.jpg'
fromWhichImgStart = '115.jpg' #"1299.jpg"

    #Numer zdjęcia do iteracji - default 0
whichImgNow = 0

    #Ilość zdjęć w liście - max 300 - default 1
listCapacity = 1

#Pobiera metadane o zdjęciach: z folderu o id-q, bez skasowanych-trashed, posegrewowane po tytule-orderBy (tutaj nie title tylko title_natural aby sortowało pokolei a nie alfabetycznie, czyli ->1,10,100,1000,2,20...), maksymalna ilość danych-maxResults (lista potrafi przechować max 300)
found_first_image = 0
imgCell = "H" + str(cellNumber)
howManyImg = wks.acell(imgCell).value
imgSrcString = ''

for file_list in dc.ListFile({'q': string_folder_id, 'orderBy': 'title_natural', 'maxResults': listCapacity}):
    #print('Received %s files from Files.list()' % len(file_list))
    #Pomija jeżeli chcemy zacząć od póżniejszej komórki
    whichImgNow += 1
    print('Image:  %s ' % whichImgNow)

    if(file_list[0]['title'] == fromWhichImgStart or found_first_image):
        if(found_first_image == 0):
            found_first_image = 1
            print("jest git")

        #Sprawdzenie czy nazwa zdjęcia z googledrive zgadza się z numerem inkrementacji kolejnych zdjęć w kodzie
        fromWhichImgStart = str(whichImgNow) + ".jpg"
        if(file_list[0]['title'] == fromWhichImgStart):
            imgSrcString += 'https://drive.google.com/uc?export=download&id=' + file_list[0]['id']
        

            if(int(howManyImg) > 1):

                if(howManyImg == '2'):
                    howManyImg = '1'
                elif(howManyImg == '3'):
                    howManyImg = '2'
                elif(howManyImg == '4'):
                    howManyImg = '3'

                imgSrcString += '|'
            else:
                wks.update(imgCell, imgSrcString)
                imgSrcString = ''
                cellNumber += 1
                imgCell = "H" + str(cellNumber)
                howManyImg = wks.acell(imgCell).value
                while(howManyImg == '0'):
                    cellNumber += 1
                    imgCell = "H" + str(cellNumber)
                    howManyImg = wks.acell(imgCell).value
        else:
            print("Pobralo zle zdjecie -> pobrało " + file_list[0]['title'] + " zamiast " + str(whichImgNow) + ".jpg")
            temp = int((file_list[0]['title']).partition('.')[0])
            if(whichImgNow > int((file_list[0]['title']).partition('.')[0])):
               print("Pobrane zdjęcie jest mniejsze")
               whichImgNow-=1
               manual_error_manager()
            else:
              print("Pobrane zdjęcie jest większe - jeżeli coś takieg się wykona trzeba zaimplementować rozwiązanie")
              manual_error_manager()

        

"""
file_list = dc.ListFile({'q': "'1-bMZmyepd1FITJdv6mv-b5lU-7wiiNWz' in parents and trashed=false", 'orderBy': 'title_natural', 'maxResults': 250})
for file1 in file_list:
    imagesList.append(file1['id'])
"""

for cellNumber in range (firstCell, 400):
    imgCell = "H" + str(cellNumber)
    howManyImg = wks.acell(imgCell).value

    imgSrcString = ''
    if (howManyImg): #Przebudować na 2 if z przejściem do funkcji
        if (listCapacity - whichImgNow < int(howManyImg)-1):
            firstCell = cellNumber
            break;
        for j in range (1, int(howManyImg)+1):
            imgSrcString += 'https://drive.google.com/uc?export=download&id=' + imagesList[whichImgNow-1]
            whichImgNow += 1
            if (int(howManyImg) > 1 and int(howManyImg) != j):
                imgSrcString += '|'
        wks.update(imgCell, imgSrcString)
time.sleep(5)

#driver.quit()