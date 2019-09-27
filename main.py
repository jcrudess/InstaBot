from instabot import InstaBot
from utils import queryDB, insertDB
import time
import datetime

bot = InstaBot('TEST')
bot.login()
counter = 0

f = open("log.txt", "a")

while 1:
    counter += 1
    now = datetime.datetime.now()
    print('novi ciklus '+str(now))
    
    picLiked = bot.run(('mediterraneanfood', 'food', 'instafoodie'), 50)
    f.write(str(now)+' cycle no.'+str(counter)+', pics liked: '+str(picLiked)+'\n')
    print(str(now)+' cycle no.'+str(counter)+', pics liked: '+str(picLiked))
    time.sleep(20)
