import cv2
#print("package imported!")

#展示图片
'''
img = cv2.imread("resouces/未命名作品.png")
#cv2.imshow("output",img)
#cv2.waitKey(0)
'''


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

while True:
    success,img=cap.read()
    cv2.imshow("cap", img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
'''