import cv2
import numpy as np

img=cv2.imread("resouces/未命名作品.png")

width,height=300,300
#从左到右，从上到下
points1=np.float32([[706,87],[1223,85],[713,665],[1213,655]])
points2=np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix=cv2.getPerspectiveTransform(points1,points2)
imgOutput=cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("image",img)
cv2.imshow("output",imgOutput)

cv2.waitKey(0)