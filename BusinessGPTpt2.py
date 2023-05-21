import praw
from multiprocessing.sharedctypes import Value
from datetime import datetime
import time
import requests
from PIL import Image
from bs4 import BeautifulSoup
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

def run(redditURLSTR):

    date = datetime.now().date()
    date = date.strftime('%m-%d-%Y') # converts the date to a string
    # Sends the article list for chatgpt to read and create script
    newsCastingScript = "Tell the viewers the information in these five reddit articles " + redditURLSTR 
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are Charles Cavendish, a newscaster for the morning show: Market Rundown. remind them of your name and the date: {date}."},
            {"role": "user", "content": newsCastingScript}
        ]
    )    


    print("completion")
    # Stores the script
    news = open(f"Business_{date}.txt","w")
    news.writelines(completion.choices[0].message.content)
    news.close()

    #creates the voice for the video (elevenlabs)
    voice = user.get_voices_by_name("Charles Cavendish")[0]
    audio = voice.generate_audio_bytes(completion.choices[0].message.content)

    # Convert the audio to a supported format using pydub
    audio = AudioSegment.from_file(io.BytesIO(audio), format="mp3")
    audio.export(f"images/{date}/Business_{date}.wav", format="wav")

    videoLen = librosa.get_duration(filename=f"images/{date}/Business_{date}.wav")
    createVideoPlate(date,videoLen)


            
nameOfReddits = 'https://www.scmp.com/news/world/united-states-canada/article/3220816/theranos-co-founder-elizabeth-holmes-loses-bid-avoid-prison-gets-hit-us452-million-restitution-bill https://www.cnbc.com/2023/05/17/why-so-many-people-making-100000-dollars-a-year-dont-feel-rich.html https://www.cnn.com/2023/05/17/economy/debt-ceiling-political-football/index.html https://www.reuters.com/business/autos-transportation/chinas-geely-invest-295-mln-aston-martin-2023-05-18/?utm_source=reddit.com https://thedailyny.com/2023/05/18/bt-plans-to-reduce-its-workforce-by-55000-jobs-and-it-is-expected-that-ai-will-replace-up-to-20-of-those-positions/ https://www.theguardian.com/business/2023/may/17/ubs-make-35bn-credit-suisse-takeover-lose-17bn-rushed-deal'
run(nameOfReddits)
