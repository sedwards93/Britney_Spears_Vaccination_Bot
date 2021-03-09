import random
import time
import tweepy
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from os import environ
from lxml import html
import requests
from twitter import OAuth, Twitter


For Heroku
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# For local
# import credentials
# CONSUMER_KEY = credentials.CONSUMER_KEY
# CONSUMER_SECRET = credentials.CONSUMER_SECRET
# ACCESS_KEY = credentials.ACCESS_KEY
# ACCESS_SECRET = credentials.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) 
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

INTERVAL = 60 * 60 * 12  # tweet every 12 hours
# INTERVAL = 15  # every 15 seconds, for testing

class BritneyBot:
    def __init__(self):
        self.url = 'https://coronavirus.data.gov.uk/details/vaccinations'
        self.number = 0
        self.youtube = 'https://youtu.be/PZYSiWHW8V0'

    def scrape_corona(self):
        op = webdriver.ChromeOptions()
        op.binaray_location = os.environ.get("GOOGLE_CHROME_BIN")
        op.add_argument("--headless")
        op.add_argument("--no-sandbox")
        op.add_argument("--disable-dev-sh-usage")
        bot = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
        bot.get(self.url)
        time.sleep(3)
        element = bot.find_elements_by_xpath('//*[@id="value-item-people_vaccinated-first_dose_total-cumpeoplevaccinatedfirstdosebypublishdate-0_modal"]')
        element = element[0]
        regex = re.compile(r'\d\d+,\d\d\d+,\d\d\d+')
        number = regex.search(element.text)
        self.number = number.group()
        bot.close()
        
    def sample(self):
        videos = ['https://youtu.be/PZYSiWHW8V0', 'https://youtu.be/clwLKJ294u4', 'https://youtu.be/elueA2rofoo','https://youtu.be/u4FF6MpcsRw', 'https://youtu.be/LOZuxwVk7TU', 'https://youtu.be/Mzybwwf2HoQ', 'https://youtu.be/AJWtLf4-WWs']
        self.youtube = random.choice(videos)

    def tweet(self):
         self.sample()
         api.update_status(f'{self.number} people in the UK have received their first COVID-19 vaccine dose...\n\nYet Britney still doesn\'t have her freedom?!\n\n#FREEBRITNEY\n\n{self.youtube} via @YouTube')

    def search(self):
        search = '#freebritney'
        nrTweets = 300
        for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
            try:
                tweet.favorite()
                print('Tweet Liked')
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
                
            

britneybot = BritneyBot()
while True:
    print("About to fetch vaccine information")
    britneybot.scrape_corona()
    print("About to tweet")
    britneybot.tweet()
    print("About to search and favourite")
    britneybot.search()
    print("About to sleep for set interval")
    time.sleep(INTERVAL)
    print("About to search and favourite")
    britneybot.search()
    print("About to sleep for set interval")
    time.sleep(INTERVAL)




    