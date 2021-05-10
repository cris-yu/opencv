import cv2
import numpy as np

framewidth=640
frameheight=480
cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

mycolor=[[5,107,0,19,255,255],#识别不同的颜色
          [133,56,0,159,156,255],
          [57,76,0,100,255,255]]

mycolorval=[[255,153,51],
            [255,0,255],
            [0,250,0]]

mypoints= []        #[x,y,colorsid]

def findcolor(img,mycolor,mycolorval):
    imgHsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoint=[]
    for color in mycolor:
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv2.inRange(imgHsv,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgresult,(x,y),10,mycolorval[count],cv2.FILLED)#画点
        if x!=0and y!=0:
            newpoint.append([x,y,count])
        count+=1
        #cv2.imshow(str(color[0]),mask)
    return newpoint

def getContours(img):#检测物体并描边
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)
        if area>500:
            #cv2.drawContours(img,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(mypoints,mycolorval):
    for point in mypoints:
        cv2.circle(imgresult,(point[0],point[1]),10,mycolorval[point[2]],cv2.FILLED)

while True:
    success,img=cap.read()
    imgresult=img.copy()
    newpoint=findcolor(img,mycolor,mycolorval)
    if len(newpoint)!=0:
        for newP in newpoint:
            mypoints.append(newP)
    if len(mypoints)!=0:
        drawoncanvas(mypoints,mycolorval)


    cv2.imshow("result",imgresult)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break