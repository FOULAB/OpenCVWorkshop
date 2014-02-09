#Simple example showing getRotationMatrix2D and warpAffine

import cv2
import time

w = 5

cv2.namedWindow("camera", cv2.CV_WINDOW_AUTOSIZE)

framecounter = 0
capture = cv2.VideoCapture(0)
ret = False;
while(not ret):
  ret,img = capture.read()
  
c = img.shape[0];
r = img.shape[1];

while True:
 
    framecounter = framecounter + 1

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rotMat = cv2.getRotationMatrix2D((r/2,c/2), w * framecounter, 1.0)
    imgRotate = cv2.warpAffine(imgGray, rotMat,(r,c))

    cv2.imshow("camera", imgRotate)
    
    ret = False
    while(not ret):
       ret,img = capture.read()
       
    if cv2.waitKey(10) == 27:
        break
