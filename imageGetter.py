import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime


def createImgBank(date,URL,count,imageNum):
    getURL = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(getURL.text, 'html.parser')

    images = soup.find_all('img')
    resolvedURLs = []

    for image in images:
        src = image.get('src')
        resolvedURLs.append(requests.compat.urljoin(URL, src))

    if not os.path.exists(f'images/{date}/'):  
        os.makedirs(f'images/{date}/')

    for i in range(1,imageNum):
        image = resolvedURLs[i]
        webs = requests.get(image)
        open(f'images/{date}/' + f'{count+i}' +".jpg", 'wb').write(webs.content)


# date = datetime.now().date()
# date = date.strftime('%m-%d-%Y')



    