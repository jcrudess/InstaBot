from utils import getUnfollowList
import datetime
from selenium import webdriver
import time

now = datetime.datetime.now()
driver = webdriver.Firefox()
driver.get("https://www.instagram.com")
time.sleep(1)
log_inButton = driver.find_element_by_css_selector('.izU2O > a:nth-child(1)').click()
userField = driver.find_element_by_css_selector('div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
passField = driver.find_element_by_css_selector('div.-MzZI:nth-child(3) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)')
userField.send_keys('crofoodjunkie')
passField.send_keys('Kosarka.1')
submitButton = driver.find_element_by_css_selector('.L3NKy').click()
print('login success')
time.sleep(3)
curDate = str(now.year)+'-'+f"{now.month:02d}"+'-'+ f"{now.day:02d}"
curDate = '2019-09-25'
followedList = [user[0] for user in getUnfollowList(curDate)]
driver.find_element_by_css_selector('button.aOOlW:nth-child(2)').click()
time.sleep(5)
#dohvati listu followera
driver.get("https://www.instagram.com/crofoodjunkie/")
driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a').click()
time.sleep(5)
followerListElement = driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li/div/div[2]/div[1]/div/div/a')
followerList = [user.text for user in followerListElement]
driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[2]/button/span').click()
time.sleep(2)
#otvori following listu i provjeravaj
driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a').click()
time.sleep(5)
recentList = driver.find_elements_by_xpath("/html/body/div[3]/div/div[2]/ul/div/li") 

for list in recentList :
    driver.execute_script("arguments[0].scrollIntoView();", list )
time.sleep(1)
# for user in driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li/div'):
#     username = user.find_element_by_xpath('div[2]/div[1]/div/div/a').text
#     print(username)
    # if username in followedList and username not in followerList:
    #      user.find_element_by_xpath('div[3]/button').click()
    #      time.sleep(10)


