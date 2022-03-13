import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
servie=Service(ChromeDriverManager().install())

import warnings
warnings.filterwarnings('ignore')


def blackboardGetCalendar(user_id,passwd,bb_link):

    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    browser = webdriver.Chrome(service=servie,options=options)
    blackboard_link = bb_link
    browser.get(blackboard_link)
    username = browser.find_element_by_id("user_id")
    password = browser.find_element_by_id("password")
    
    username.send_keys(user_id)
    password.send_keys(passwd)
    #Click on calendar button
    browser.find_element_by_xpath("/html/body/div/div/div/form/ul/li[4]").click()
    time.sleep(3)

    #Get icalendar link
    browser.find_element_by_link_text("Calendar").click()
    time.sleep(3)
    browser.find_element_by_id('ical').click()
    time.sleep(3)
    icalurl = browser.find_element_by_id('icalurlid').text
    
    # Download Calendar
    browser.get(icalurl) 
    time.sleep(1)  
    os.rename(os.path.join(os.getcwd(), "learn.ics"), os.path.join(os.getcwd(), user_id + ".ics"))