import cv2
import numpy as np

widthimg = 640
heightimg = 480

cap = cv2.VideoCapture(0)
cap.set(90, 800)


def preprocessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((9, 9))
    imgDial = cv2.dilate(imgCanny, kernel, iterations = 2)
    imgThres = cv2.erode(imgDial, kernel, iterations = 1)
    return imgThres


def getContours(img):  # 检测物体并描边
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            # cv2.drawContours(imgcontour,cnt,-2,(255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgcontour, biggest, -2, (255, 0, 0), 20)
    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis = 1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew


def getwrap(img, biggest):
    biggest = reorder(biggest)
    points1 = np.float32(biggest)
    points2 = np.float32([[0, 0], [widthimg, 0], [0, heightimg], [widthimg, heightimg]])
    matrix = cv2.getPerspectiveTransform(points1, points2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthimg, heightimg))

    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv2.resize(imgCropped, (widthimg, heightimg))

    return imgCropped


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (
                        imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(
                    imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


while True:
    success, img = cap.read()
    img = cv2.resize(img, (widthimg, heightimg))
    imgcontour = img.copy()

    imgThres = preprocessing(img)
    biggest = getContours(imgThres)
    # print(biggest)
    if biggest.size != 0:
        imgwarp = getwrap(img, biggest)
        imgarray = ([img, imgThres], [imgcontour, imgwarp])
    # cv2.imshow ("cap" , imgwrapped)
    else:
        imgarray = ([imgcontour, img])

    stackimages = stackImages(0.6, imgarray)
    cv2.imshow("workflow", stackimages)
    #cv2.imshow("imagewrap", imgwarp)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
