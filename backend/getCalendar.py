import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
servie=Service(ChromeDriverManager().install())
from icalendar import Calendar
import os
import sqlite3
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
    time.sleep(3)


class Conv():
    
    def __init__(self):
        self.data = []
        self.calendar = None
        
    def read_calendar(self,location_calendar):
        with open(location_calendar,'r') as cal_file:
            cal_data = cal_file.read()
        self.calendar = Calendar.from_ical(cal_data)
        return self.calendar
    
    def conv_to(self):
        
        for event in self.calendar.subcomponents:
            if event.name != 'VEVENT':
                continue
            data_row = [
                event.get('SUMMARY'),
                event.get('DTEND').dt
                # event.get('DESCRIPTION') 
                ]
            data_row = [str(x) for x in data_row]
            self.data.append(data_row)  

                        
    def write_sql(self,id):
        
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM deadline where user_id = %s and from_bb = 1" % id)

        for line in self.data:
            cursor.execute("INSERT INTO deadline (name,time,from_bb,set_reminder,user_id) VALUES ('%s', '%s', 1, 0, %d)" % (line[0],line[1][:line[1].find('+')],id))
        
        connection.commit()
        connection.close()


def syncDeadlines(id, stu_id,passwd):
    
    blackboardGetCalendar(stu_id,passwd,'https://bb.cuhk.edu.cn')
    conv = Conv()
    conv.read_calendar('learn.ics')
    conv.conv_to()
    conv.write_sql(id)
    os.remove('learn.ics')