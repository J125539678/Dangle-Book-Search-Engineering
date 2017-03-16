# -*- coding:gbk -*-

import cv2
from math import *
import os
import os.path

def hash5(exam):
    return exam
def hash4(exam):
    return exam[0] +exam[2]+exam[5] +exam[8]+exam[10] +exam[12] +exam[14] +exam[16]+exam[19]+exam[20]+exam[11] +exam[9]+exam[22] +exam[24] +exam[25]+exam[1] +exam[4]
def hash3(exam):
    return exam[0] +exam[2]+exam[5] +exam[8]+exam[10] +exam[12] +exam[14] +exam[16]+exam[19]+exam[20]+exam[11] +exam[9]+exam[22] +exam[24] +exam[25]
def hash2(exam):
    return exam[0] +exam[2]+exam[5] +exam[8]+exam[10] +exam[15] +exam[18] +exam[20]+exam[22]+exam[26]+exam[12]+exam[14]
def hash1(exam):
    return exam[0] +exam[4]+exam[15] +exam[20] +exam[25]+exam[2]+exam[5]+exam[13]+exam[18]

def quality(img):
    a = len(img)
    h = len(img[0])
    a1 = int(a/2)
    a2 = a - a1
    h1 = int (h/2)
    h2 = h - h1

    magn = []
    anoneed=[]
    hnoneed=[]

    for i in range(a):
        for j in range(h):
            if (j==h-1):
                anoneed.append(i)
            if (img[i][j][0]==255 and img[i][j][1]==255 and img[i][j][2]==255):
                continue
            else:
                break

    for i in range(h):
        for j in range(a):
            if (j==a-1):
                hnoneed.append(i)
            if (img[j][i][0]==255 and img[j][i][1]==255 and img[j][i][2]==255):
                continue
            else:
                break

    r=0
    g=0
    b=0
    for i in range (a1):
        for j in range (h1):
            if (i in anoneed) or (j in hnoneed):
                continue
            m=i
            n=j
            r = r + img[m][n][0]
            g = g + img[m][n][1]
            b = b + img[m][n][2]
    magn.append(float(r)/(r+g+b))
    magn.append(float(g)/(r+g+b))
    magn.append(float(b)/(r+g+b))

    r=0
    g=0
    b=0
    for i in range (a2):
        for j in range (h1):
            if (i in anoneed) or (j in hnoneed):
                continue
            m=i+a1
            n=j
            r = r + img[m][n][0]
            g = g + img[m][n][1]
            b = b + img[m][n][2]
    magn.append(float(r)/(r+g+b))
    magn.append(float(g)/(r+g+b))
    magn.append(float(b)/(r+g+b))

    r=0
    g=0
    b=0
    for i in range (a1):
        for j in range (h2):
            if (i in anoneed) or (j in hnoneed):
                continue
            m=i
            n=j+h1
            r = r + img[m][n][0]
            g = g + img[m][n][1]
            b = b + img[m][n][2]
    magn.append(float(r)/(r+g+b))
    magn.append(float(g)/(r+g+b))
    magn.append(float(b)/(r+g+b))

    for i in range (a2):
        for j in range (h2):
            if (i in anoneed) or (j in hnoneed):
                continue
            m=i+a1
            n=j+h1
            r = r + img[m][n][0]
            g = g + img[m][n][1]
            b = b + img[m][n][2]
    magn.append(float(r)/(r+g+b))
    magn.append(float(g)/(r+g+b))
    magn.append(float(b)/(r+g+b))

    q=[]
    for (i,e) in enumerate(magn):
            t = e
            if t<0.2:
                q.append(0)
                q.append(0)
                q.append(0)
            elif t>=0.2 and t<0.25:
                q.append(1)
                q.append(0)
                q.append(0)
            elif t>=0.25 and t<0.3:
                q.append(0)
                q.append(1)
                q.append(0)
            elif t>=0.3 and t<0.33:
                q.append(1)
                q.append(1)
                q.append(0)
            elif t>=0.33 and t<0.3345:
                q.append(0)
                q.append(0)
                q.append(1)
            elif t>=0.3345 and t<0.336:
                q.append(1)
                q.append(1)
                q.append(1)
            elif t>=0.336 and t<0.50:
                q.append(1)
                q.append(0)
                q.append(1)
            elif t>=0.50 and t<0.55:
                q.append(0)
                q.append(1)
                q.append(1)
            else:
                q.append(1)
                q.append(1)
                q.append(1)
    return q

def search(aim):
    detector = cv2.SIFT()
    orb = cv2.ORB()
    file = open("true_quality_binary.txt")
    contents = file.read().split("\n")
    file.close()

    qual=[]
    nam = []
    for i in contents:
        tmp = i.split(" ")

        name = tmp[0]
        q = tmp[1]
        qual.append(q)
        nam.append(name)
    img = cv2.imread('static/searchpic/'+aim, cv2.IMREAD_COLOR)
    aim_list = quality(img)
    aim_qual = ""
    for i in aim_list:
        aim_qual = aim_qual+str(i)

    similar_list=[]
    for (i,ele) in enumerate(qual):
        number = 0
        if hash1(ele)==hash1(aim_qual):
            similar_list.append(i)
    if len(similar_list)>50:#2222222222222
        similar_list=[]
        for (i,ele) in enumerate(qual):
            number = 0
            if hash2(ele)==hash2(aim_qual):
                similar_list.append(i)
        if len(similar_list)>50:#3333333333
            similar_list=[]
            for (i,ele) in enumerate(qual):
                number = 0
                if hash3(ele)==hash3(aim_qual):
                    similar_list.append(i)
            if len(similar_list)>50:#44444444444
                similar_list=[]
                for (i,ele) in enumerate(qual):
                    number = 0
                    if hash4(ele)==hash4(aim_qual):
                        similar_list.append(i)
                if len(similar_list)>50:#5555555555
                    similar_list=[]
                    for (i,ele) in enumerate(qual):
                        number = 0
                        if hash5(ele)==hash5(aim_qual):
                            similar_list.append(i)
    # print aim
    # img = cv2.imread(aim, cv2.IMREAD_COLOR)
    keypoints1 = detector.detect(img,None)
    mmax = 0
    for i in keypoints1:
        if (i.response < 0.04):
            keypoints1.remove(i)
    kp, des = cv2.SIFT().detectAndCompute(img, None)
    x = 0

    resu={}
    numb=[]
    for gray1 in similar_list:
        x = x+1
        gray2 = cv2.imread('picturedata/'+nam[gray1],cv2.IMREAD_GRAYSCALE)
        kp1,des1  = cv2.SIFT().detectAndCompute(gray2, None)
        matches = cv2.BFMatcher().knnMatch(des, des1, k = 2)
        great = 0
        for i,j in matches:
            if i.distance<0.75*j.distance:
                great = great+1
        resu[great]=gray1
        numb.append(great)
        if (great>mmax):
            mmax = great
            taget = gray2
            name = nam[gray1]
            kp2,des2 =kp1,des1
    numb.sort()
    numb.reverse()
    if len(numb)>25:
        numb=numb[0:25]
    for i,e in enumerate(numb):
        if e<8:
            numb=numb[:i]
    final_name=[]
    for i in numb:
        final_name.append(nam[resu[i]])

    f = open("index.txt")
    file = f.read()
    f.close()

    list = []
    file = file.split("\n")
    for i in final_name:
        j = file.index(i)
        l = []
        l.append(file[j+1])
        l.append(file[j+2][6:])
        l.append(file[j+3][7:])
        l.append(file[j+4][6:])
        list.append(l)
    return list
