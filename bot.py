import random
import time
import tweepy
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from lxml import html
import requests
from twitter import OAuth, Twitter
import credentials

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET) 
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
api = tweepy.API(auth)

class BritneyBot:
    def __init__(self):
        self.url = 'https://coronavirus.data.gov.uk/details/vaccinations'
        self.number = 0
        self.youtube = 'https://youtu.be/PZYSiWHW8V0'

    def scrape_corona(self):
        bot = webdriver.Firefox()
        bot.get(self.url)
        time.sleep(3)
        element = bot.find_elements_by_xpath('//*[@id="value-item-people_vaccinated-first_dose_total-cumpeoplevaccinatedfirstdosebypublishdate-0_modal"]')
        element = element[0]
        regex = re.compile(r'\d\d+,\d\d\d+,\d\d\d+')
        number = regex.search(element.text)
        self.number = number.group()
        bot.close()
        
    def sample(self):
        videos = ['https://youtu.be/PZYSiWHW8V0','https://youtu.be/elueA2rofoo','https://youtu.be/u4FF6MpcsRw', 'https://youtu.be/LOZuxwVk7TU']
        self.youtube = random.choice(videos)

    def tweet(self):
         self.sample()
         api.update_status(f'{self.number} people in the UK have received their first COVID-19 vaccine dose...\n\nYet Britney still doesn\'t have her freedom?!\n\n#FREEBRITNEY\n\n{self.youtube} via @YouTube')


britneybot = BritneyBot()
britneybot.scrape_corona()
britneybot.tweet()


    