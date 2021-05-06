import cv2
import numpy as np
#print("package imported!")

#展示图片

img = cv2.imread("resouces/未命名作品.png")
kernel=np.ones((5,5),np.uint8)

#灰度模式
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#模糊模式
imgBlur=cv2.GaussianBlur(imgGray,(23,23),0)
#线条模式
imgCanny=cv2.Canny(img,100,100)
#线条扩充
imgDialation=cv2.dilate(imgCanny,kernel,iterations=1)
#线条减弱
imgErode=cv2.erode(imgDialation,kernel,iterations=1)

cv2.imshow("output1",imgGray)
cv2.imshow("output2",imgBlur)
cv2.imshow("output3",imgCanny)
cv2.imshow("output4",imgDialation)
cv2.imshow("output5",imgErode)
cv2.waitKey(0)



#放视频
'''
cap=cv2.VideoCapture("resouces/fingers.mov")
while True:
    success,img=cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
'''

#调用摄像头
'''
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(90,800)

while True:
    success,img=cap.read()
    cv2.imshow("cap", img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
'''