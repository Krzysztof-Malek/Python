import requests #for sending web requests
import json
import psutil   #for getting laptop status
import time
import schedule #for scheduling actions

#URL for webhooks to turn off/on smart plug
webhook_url_plugOff = 'https://maker.ifttt.com/trigger/battery_off/with/key/drviQp5SGVT752k8_UfbxnBjQOkca8XQ6kkM6GEex8q'
webhook_url_plugOn = 'https://maker.ifttt.com/trigger/battery_on/with/key/drviQp5SGVT752k8_UfbxnBjQOkca8XQ6kkM6GEex8q'

#Check if laptop is being charged and its' battery level
def check_battery():
    batteryInfo = psutil.sensors_battery()
    plugged = batteryInfo.power_plugged
    percent = str(batteryInfo.percent)
    isItOnDesk = 0

    #If battery less than 30 and not charging
    if(int(percent) < 30 and not plugged):
        r = requests.post(webhook_url_plugOn)
        time.sleep(5)
        plugged = psutil.sensors_battery().power_plugged
        #Checks if the laptop is physicaly pluged to charger (is on desk)
        while(not plugged and isItOnDesk < 3):
            r = requests.post(webhook_url_plugOn)
            time.sleep(10)
            plugged = psutil.sensors_battery().power_plugged
            isItOnDesk += 1
        #If it's not on desk smart plug is turning off
        if(isItOnDesk > 2 and not plugged):
            r = requests.post(webhook_url_plugOff)
    #If battery more than 80 and plugged
    elif(int(percent) > 80 and plugged):
        r = requests.post(webhook_url_plugOff)

#Check the laptop status on the beginning of program (30s for laptop to turn on)
time.sleep(30)
check_battery()

#Checks battery every 3 minutes
schedule.every(3).minutes.do(check_battery)

#Loop for program to run it constantly
while 1:
   schedule.run_pending()
   time.sleep(5)
