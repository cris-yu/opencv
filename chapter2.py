import cv2
import numpy as np

img=cv2.imread("resouces/未命名作品.png")
print(img.shape)
#重置尺寸
imgResize=cv2.resize(img,(3400,2400))
#裁切
imgCropped=img[0:300,200:500]

cv2.imshow("Image",img)
cv2.imshow("image resize",imgResize)
cv2.imshow("Image cropped",imgCropped)
cv2.waitKey(0)