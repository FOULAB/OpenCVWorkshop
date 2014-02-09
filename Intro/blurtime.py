

import cv2
import time

cv2.namedWindow("camera", cv2.CV_WINDOW_AUTOSIZE)

capture = cv2.VideoCapture(0)

ret = False
while(not ret):
  ret,img = capture.read()
  
c = img.shape[0]
r = img.shape[1]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgAvg = imgGray[:]

while True:
    alpha = 0.1
    imgAvg = cv2.addWeighted(imgAvg, 1.0 - alpha, imgGray, alpha, 0.0)
    
    cv2.imshow("camera", imgAvg)
    
    ret = False
    while(not ret):
      ret,img = capture.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if cv2.waitKey(10) == 27:
        break
