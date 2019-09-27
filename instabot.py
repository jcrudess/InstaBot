import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from bs4 import BeautifulSoup
from utils import *
import random

class InstaBot:
    def __init__(self, modul):
        self.user = readConfig(modul, 'user')
        self.password = readConfig(modul, 'pass')
        self.waitTime = readConfig(modul, 'wait_time')
        print(self.waitTime)
        self.startURL = readConfig('DEFAULT', 'instaURL')
        self.listCounter = 0
        self.driver = switchProxyUA()
        self.usersFollowed = 0

    def login(self):
        self.driver.get(self.startURL)
        time.sleep(10)
        log_inButton = self.driver.find_element_by_css_selector('.izU2O > a:nth-child(1)')
        log_inButton.click()
        time.sleep(10)
        userField = self.driver.find_element_by_css_selector('div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
        passField = self.driver.find_element_by_css_selector('div.-MzZI:nth-child(3) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
        userField.send_keys(self.user)
        passField.send_keys(self.password)
        submitButton = self.driver.find_element_by_css_selector('.L3NKy')
        submitButton.click()
        print('login success')
        time.sleep(10)
        try:
            smece = self.driver.find_element_by_css_selector('button.aOOlW:nth-child(2)')
            smece.click()
        except:
            time.sleep(2)

    def run(self, tagList, likesPH):
        picLiked = 0
        folCount = 0
        hourReport = 0
        hourLastProxySwitch = datetime.datetime.now().hour
        for tag in tagList:
            writeDetailLog('radim hashtag '+tag)
            self.driver.get(self.startURL+'/explore/tags/'+tag)
            for i in range(1, 7):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
            hrefs = self.driver.find_elements_by_tag_name('a')
            links = [elem.get_attribute('href') for elem in hrefs]
            picLinks = [href for href in links if '/p/' in href]
            for link in picLinks:
                #promijeni proxy
                if datetime.datetime.now().hour != hourLastProxySwitch:
                    writeDetailLog('mijenjam proxy')
                    self.driver.quit()
                    print('mijenjam proxy')
                    self.listCounter += 1
                    if self.listCounter == 5:
                        self.listCounter = 0
                    self.driver = switchProxyUA()
                    self.login()
                    hourLastProxySwitch = datetime.datetime.now().hour
                    self.spavaj()
                if queryCHKLink(link) is None:
                    try:
                        self.driver.get(link)
                        insertCHKLink(link)
                        self.spavaj()
                        userPosted = self.driver.find_element_by_xpath('/html/body/span/section/main/div/div/article/header/div[2]/div[1]/div[1]/h2/a').get_attribute('title')
                        folCount = self.getFollowerCount(userPosted)
                        self.spavaj()
                        if folCount < 5000:
                            self.driver.get(link)
                            time.sleep(10)
                            likeBut = self.driver.find_element_by_css_selector('span[aria-label=Like]')
                            likeBut.click()
                            insertDB(link)
                            writeDetailLog('liked '+link)
                            picLiked += 1
                            if (datetime.datetime.now().hour != hourReport):
                                try:
                                    writeDetailLog('dosad likeano: '+str(picLiked))
                                    writeDetailLog('dosad followano: '+str(self.usersFollowed))
                                    hourReport = int(datetime.datetime.now().hour)
                                except Exception as e:
                                    time.sleep(10)
                            self.spavaj()
                        else:
                            writeDetailLog('user ima vise od max followera, preskacem like '+link)
                            self.spavaj()
                    except Exception as e:
                        writeDetailLog('Greska na likeanju '+link+': '+str(e))
                        self.spavaj()
                        continue
                else:
                    writeDetailLog(link + ' ' + 'je vec posjecen!')
                    continue
        return picLiked

    def getFollowerCount(self, user):
        if queryUserDB(user) is not None:
            writeDetailLog('user '+user+' already followed!')
            return 1
        
        if queryCHKUser(user) is None:
            self.driver.get(self.startURL+"/"+user+"/")
            self.spavaj()
            count = self.driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span").text
            countInt = int(count.replace(',', '').replace('k','000').replace('.','').replace('m', '000000'))
            if countInt > 5000:
                insertCHKUser(user)
                return 1000000
                #follow user
            self.driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
            writeDetailLog('user '+user+' new follow')
            self.usersFollowed += 1
            insertUserDB(user)
            insertCHKUser(user)
            time.sleep(10)
            return countInt
        else:
            writeDetailLog('user '+user+' already visited!')
            return 1000000

    def spavaj(self):
        sleeptime = int(self.waitTime)
        time.sleep(random.randint(sleeptime, sleeptime+10))
                

            

        
        