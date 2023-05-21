from moviepy.editor import *
from PIL import Image
import cv2
import os, os.path
from datetime import datetime
import numpy
import copy
import math

def createBackground(back):
    h, w, c = back.shape
    for row in range(h):
        for col in range(w):
            # print(f"{row} and {col}")
            back[row][col][0] = 200
            back[row][col][1] = 200
            back[row][col][2] = 200
    return back
def addImageToVideo(background, image, x,y):
    h1,w1,c1 = background.shape
    # print(h1)
    # print(w1)
    h, w, c = image.shape
    imageCopy = copy.deepcopy(image)
    backgroundCopy = copy.deepcopy(background)
    # print(h)
    # print(w)
    for row in range(h):
        for col in range(w):
            # print(f"{row} and {col}")
            imgRow = int(y-h/2+row)
            imgCol = int(x-w/2+col)
            backgroundCopy[imgRow][imgCol][0] = imageCopy[row][col][0]
            backgroundCopy[imgRow][imgCol][1] = imageCopy[row][col][1]
            backgroundCopy[imgRow][imgCol][2] = imageCopy[row][col][2]
    return backgroundCopy

def createVideoPlate(date,videoLen):
    imageSize = (1080,1920)
    imageArray = []
    import os, os.path

    imgs = []
    # date = datetime.now().date()
    path = f"images/{date}/"
    valid_images = [".jpg",".gif",".png",".tga"]
    print(path)
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path,f)))

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter(f'images/{date}/video.avi', fourcc, 24, imageSize, isColor=True)
    for i in range(24):
        background = Image.open(os.path.join(f"background/b{0}.jpeg"))
        background = numpy.asarray(background)
        background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
        out.write(background)
    for i in range(len(imgs)):
        print(f"--------{i}---------") 
        for n in range(int(math.ceil(((videoLen-1)*24)/len(imgs)))):
            img = imgs[i]
            num = n%139
            background = Image.open(os.path.join(f"background/b{num+1}.jpeg"))
            background = numpy.asarray(background)
            background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
            


            img = numpy.asarray(img)
            shape = img.shape
            img = cv2.resize(img,(shape[1]*3,shape[0]*3))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # pt11 = (int(540-(shape[1]*3)/2),int(890-(shape[0]*3)/2))
            # pt22 = (int(540+(shape[1]*3)/2),int(890+(shape[0]*3)/2))
            # background = cv2.rectangle(background, pt1=pt11, pt2=pt22, color=(255,255,255), thickness=-1)
            img2 = addImageToVideo(background,img,540,890)
            out.write(img2)
    out.release()
# date = datetime.now().date()
# date = date.strftime('%m-%d-%Y')
# createVideoPlate("04-14-2023", 78)
 