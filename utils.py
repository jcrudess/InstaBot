import configparser
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
import random

UAlist = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1']
lastProxy = ""

def readConfig(group, setting):
    c = configparser.ConfigParser()
    c.read('config.ini')
    return c[group][setting]

def queryDB(link):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (link,)
    c.execute('SELECT * FROM links WHERE link=?', t)
    return c.fetchone()

def insertDB(link):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (link,)
    c.execute("INSERT INTO links VALUES (?)", t)
    conn.commit()
    
def writeDetailLog(text):
    now = datetime.datetime.now()
    date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    f = open('detaillog'+date+'.txt', 'a')
    print(text)
    f.write(str(str(now.hour)+':'+str(now.minute)+':'+str(now.second))+'-- '+text+'\n')

def insertUserDB(username):
    conn = sqlite3.connect('log.db')
    now = datetime.datetime.now()
    date = f"{now.day:02d}"+f"{now.month:02d}"+str(now.year)
    t=(username, date)
    c = conn.cursor()
    c.execute('INSERT INTO USERS_FOLLOWED VALUES (?, ?)', t)
    conn.commit()

def queryUserDB(username):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (username,)
    c.execute('SELECT * FROM USERS_FOLLOWED WHERE USER = ?', t)
    return c.fetchone()

def getUnfollowList(currentDate):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (currentDate,)
    c.execute('SELECT user FROM USERS_FOLLOWED WHERE date < DATE(?, "-3 day")', t)
    return c.fetchall()

def insertCHKUser(user):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (user,)
    c.execute('INSERT INTO users_visited VALUES(?)', t)
    conn.commit()

def insertCHKLink(link):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (link,)
    c.execute('INSERT INTO posts_visited VALUES(?)', t)
    conn.commit()

def queryCHKUser(username):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (username,)
    c.execute('SELECT * FROM users_visited WHERE USER = ?', t)
    return c.fetchone()

def queryCHKLink(link):
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    t = (link,)
    c.execute('SELECT * FROM posts_visited WHERE link=?', t)
    return c.fetchone()

def switchProxyUA():
    proxy = getProxy()
    print(proxy['proxy']+' '+proxy['port'])
    writeDetailLog('new proxy: '+proxy['proxy']+' '+proxy['port'])
    useragent = getUA()
    print(useragent)
    writeDetailLog('new UA: '+useragent)
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.http",proxy['proxy'])
    fp.set_preference("network.proxy.http_port",int(proxy['port']))
    fp.set_preference("general.useragent.override",useragent)
    fp.update_preferences()
    driver = webdriver.Firefox(firefox_profile=fp)
    return driver

def getProxy():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    proxyFull = {}
    proxy = ""
    port = ""
    global lastProxy
    for proxyelem in soup.select('table#proxylisttable tbody tr'):
        proxy = proxyelem.select('td:nth-child(1)')[0].text
        port = proxyelem.select('td:nth-child(2)')[0].text
        if proxy == lastProxy:
            continue
        else:
            lastProxy = proxy
            proxyFull = {"proxy":proxy, "port":port}
            return proxyFull

            
def getUA():
    return UAlist[random.randint(0, len(UAlist)-1)]