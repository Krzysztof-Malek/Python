# import requests, lxml, re, json, pandas as pd, cfscrape
# from bs4 import BeautifulSoup as BS
from PIL import Image
import urllib.request
import os

# import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def manual_error_manager():
    print("Some error")
    input("Press Enter to continue...")
    input("Press Enter to continue...")


# Static strings
CHROMEDRIVER_PATH = "C:/Program Files (x86)/chromedriver.exe"
base_url_square = "https://images.google.com/?q=&tbs=iar:s"
base_url = "https://www.google.com/search?tbm=isch&q="
dir_name = "C:/Users/krzys/Desktop/Polibuda/sem. 6/BIAI/archive/train_v2/"
extension_name = ".jpg"

# Getting folder paths and names od breeds
class_folder_paths = ['C:/Users/krzys/Desktop/Polibuda/sem. 6/BIAI/archive/train_v2/' + x for x in
                      os.listdir('C:/Users/krzys/Desktop/Polibuda/sem. 6/BIAI/archive/train_v2/')]
dog_breed_names = []
for b in class_folder_paths:
    dog_breed_names.append(b.rsplit('/', 1)[1])

# Creating driver
driver = webdriver.Chrome(CHROMEDRIVER_PATH)
# try:
# Iterating through breeds
for breed in dog_breed_names:
    dog_url = base_url + breed + "%20dog"
    driver.get(dog_url)
    # Waiting for page to load
    driver.implicitly_wait(1)
    for i in range(100):  # Getting 100 images
        try:
            # Getting next element on page
            css_selector_name = ".isv-r:nth-child(" + str(i + 1) + ") .rg_i"
            img_element = driver.find_element(By.CSS_SELECTOR, css_selector_name)
            driver.execute_script("arguments[0].scrollIntoView(true);", img_element)

            # Generating name and path for image
            save_name = dir_name + breed + "/" + str(i + 1) + extension_name
            # Check if not empty
            # print(str(i) + " " + str(img_element.get_attribute('src')))
            if img_element.get_attribute('src'):
                # Saving image_url from url
                urllib.request.urlretrieve(img_element.get_attribute('src'), save_name)
                # Scaling image by width
                base_width = 224
                img = Image.open(save_name)
                w_percent = (base_width / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
                img.save(save_name)
        except:
            pass
# except:
#    manual_error_manager()
