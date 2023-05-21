import praw
from multiprocessing.sharedctypes import Value
from datetime import datetime
import time
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import openai
import os
from pydub import AudioSegment
from elevenlabslib import *
from elevenlabslib import ElevenLabsUser
import io
from imageGetter import *
from getURL import *
from videoGetter import *
import librosa


user = ElevenLabsUser("insert elevenLabs ID")
openai.api_key = "insert openai Key"
driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
user = ElevenLabsUser("insert Key")



def value_getter(item):
    return item[1]

def getKeyWords(title):
    words = title.split(" ")
    keywords = ""
    lengthOfTerms = len(words)
    if lengthOfTerms < 3:
        keywords = title
    else:
        for i in range(2):
            keywords = keywords + words[i] + " "
    return keywords


def formatGoogleQuery(title):
    searchURL = "https://www.google.com/search?q=" #&tbm=isch
    titles = title.split(" ")
    for word in titles:
        searchURL = searchURL + word + "+"
    searchURL = searchURL.removesuffix("+")
    searchURL = searchURL + "&tbm=isch"
    return searchURL

def run(names):
    #---- gets us into the subreddit ----#
    reddit = praw.Reddit(
        client_id="insert client id",
        client_secret="insert client stuff",
        user_agent=" insert user agent",
    )

    count = 0
    redPost = {}
    redTitles = {}

    RedditURLS = []
    RedditTitles = []

    articleURLS = ""
    articleTitles = []
    imageURLS = []
    date = datetime.now().date()
    date = date.strftime('%m-%d-%Y') # converts the date to a string

    #Finds all the subreddits and finds their top 10 posts
    #puts the top ten stories into articles dictionary
    for name in names:
        lim = 10
        print(name)
        newsSource = reddit.subreddit(name)

        for post in newsSource.hot(limit=lim):
            postTitle = post.title
            upvoteNum = post.score
            postID  =   post.id
            # print(postTitle)

            postURL = f'https://www.reddit.com/r/{name}/comments/{postID}'
            redPost[postURL] = upvoteNum

            keywordTitle = getKeyWords(postTitle)
            print(keywordTitle)
            redTitles[keywordTitle] = upvoteNum

    #sorts the post *article* dictionary and puts it into an array
    redPost = sorted(redPost.items(), key = value_getter)
    redTitles = sorted(redTitles.items(), key = value_getter)

    #trims the reddit urls to only top 10
    for i in range(10):
        RedditURLS.append(redPost[len(redPost)-i-1][0])
        RedditTitles.append(redTitles[len(redTitles)-i-1][0])
    #put all the reddit urls into a text format
    redditURLSTR = ""
    for i in range(min([len(RedditURLS),7])):
        # print(RedditURLS[i])
        # print(redditURLSTR)
        redditURLSTR = redditURLSTR + f"{RedditURLS[i]}" + " "
    
    #Get all the URLS
    for i in range(min([len(RedditURLS),5])):
        imageURLS.append(formatGoogleQuery(RedditTitles[i]))
    
    #Get Images from URLS and creates the correct folder for all to go into
    count = 0
    imgNum = 10
    print(redditURLSTR)
    print(imageURLS)
    for url in imageURLS:
        createImgBank(date,url,count,imgNum)
        count  = count + imgNum


    
nameOfReddits = ['Economics','economy','finance','business']
# nameOfReddits = ['finance']
run(nameOfReddits)
driver.close()