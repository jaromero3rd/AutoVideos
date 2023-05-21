import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime

#We find the articles in the reddit posts and puts the URLS into articleURLS
def getURLSFromReddit(URLS,titles):
    FullURLS = ""
    FullTitles = []
    for i in range(len(URLS)):
        URL = URLS[i]
        print(URL)
        getURL = requests.get(URL, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
        soup = BeautifulSoup(getURL.text, 'html.parser')

        links = soup.find_all('a')
        resolvedLinks = []

        for link in links:
            src = link.get('href')
            srcTxt = requests.compat.urljoin(URL, src)
            print(link)
            if "www.reddit" not in srcTxt and "apps" not in srcTxt and "alpha.reddit" not in srcTxt:
                resolvedLinks.append(srcTxt)
                break
        if len(resolvedLinks) > 0:
            FullURLS = FullURLS + resolvedLinks[0] + " "
            FullTitles.append(titles[i])
    return FullURLS, FullTitles

# URLS = [('https://www.reddit.com/r/Economics/comments/12wfvkb', 525), ('https://www.reddit.com/r/economy/comments/12wlqyd', 557), ('https://www.reddit.com/r/economy/comments/12xcbu4', 696), ('https://www.reddit.com/r/Economics/comments/12wslsf', 709), ('https://www.reddit.com/r/business/comments/12w8bu9', 745), ('https://www.reddit.com/r/economy/comments/12xo6i3', 787), ('https://www.reddit.com/r/business/comments/kurvl4', 932), ('https://www.reddit.com/r/finance/comments/12sw8j3', 940), ('https://www.reddit.com/r/Economics/comments/12xwsyd', 1086), ('https://www.reddit.com/r/business/comments/12xc653', 1457)]
# print(getURLSFromReddit(URLS))