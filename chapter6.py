import cv2
import numpy as np
def empty():
    pass

path='resouces/forest.png'
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",1640,1240)
cv2.createTrackbar("Hue Min","Trackbars",19,179,empty)#色调
cv2.createTrackbar("Hue Max","Trackbars",117,179,empty)
cv2.createTrackbar("Sat Min","Trackbars",96,255,empty)#饱和度
cv2.createTrackbar("Sat Max","Trackbars",191,255,empty)
cv2.createTrackbar("Val Min","Trackbars",16,255,empty)#明度
cv2.createTrackbar("Val Max","Trackbars",216,255,empty)

while True:
    img=cv2.imread(path)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos("Hue Min","Trackbars")
    h_max=cv2.getTrackbarPos("Hue Max","Trackbars")
    s_min=cv2.getTrackbarPos("Sat Min","Trackbars")
    s_max=cv2.getTrackbarPos("Sat Max","Trackbars")
    v_min=cv2.getTrackbarPos("Val Min","Trackbars")
    v_max=cv2.getTrackbarPos("Val Max","Trackbars")
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)
    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    imgResult=cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("original",img)
    cv2.imshow('HSV',imgHSV)
    cv2.imshow('Mask',mask)
    cv2.imshow('Result',imgResult)
    cv2.waitKey(1)