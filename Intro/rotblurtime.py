import cv
import time

framecounter = 0
w = 5
cv.NamedWindow("camera", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

img = cv.QueryFrame(capture)
(r,c) = cv.GetSize(img)

imgGray = cv.CreateImage((r,c), cv.IPL_DEPTH_8U, 1)
imgRotate = cv.CreateImage((r,c), cv.IPL_DEPTH_8U, 1)
imgAvg = cv.CreateImage((r,c), cv.IPL_DEPTH_8U, 1)
rotMat = cv.CreateMat(2,3,cv.CV_32FC1)

while True:
    img = cv.QueryFrame(capture)
    framecounter = framecounter + 1

    cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)

    cv.GetRotationMatrix2D((r/2,c/2), w * framecounter, 1.0, rotMat)
    cv.WarpAffine(imgGray, imgRotate, rotMat)

    alpha = 0.1
    cv.AddWeighted(imgAvg, 1.0 - alpha, imgRotate, alpha, 0.0, imgAvg)
    
    cv.ShowImage("camera", imgAvg)
    
    if cv.WaitKey(10) == 27:
        break
