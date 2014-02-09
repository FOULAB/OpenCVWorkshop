#!/usr/bin/env python
# This example has been copied from the opencv 2.4.6 samples
# it may have been tweaked to repair small bugs on Ubuntu 12.10

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

import numpy as np
import cv2
import sys
import math


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_shapes(img):
    img = cv2.GaussianBlur(img, (15, 15), 0)
    squares = []
    circles = []
    other = []
    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #for gray in cv2.cvtColor(img,cv2.COLOR_RGB2GRAY):  #cv2.split(img):
    for q in [0]:
        for thrs in [0]:   #xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 200, 230, apertureSize=5)
                #bin = cv2.dilate(bin, None)
                cv2.imshow('canny',bin)
                cv2.waitKey()
                cv2.destroyWindow('canny')
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                area=cv2.contourArea(cnt)
                if(area>=1000):
                   print "Contour:",len(cnt),cnt_len,area,abs(cnt_len/math.sqrt(area) -2*math.sqrt(math.pi))
                if(area < 1000):
                   #other.append(cnt)
                   # ignore speckles
                   pass
                elif len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
                    else:
                        other.append(cnt)
                else:
                    # perimeter to sqroot area ratio is two x sqrt(pi)
                    if(abs(cnt_len/math.sqrt(area)-2*math.sqrt(math.pi)) < 0.5):
                        circles.append(cnt)
                    else: 
                        other.append(cnt)
    return squares,circles,other

if __name__ == '__main__':
    from glob import glob
    for fn in sys.argv[1:]:
        img = cv2.imread(fn)
        squares,circles,other = find_shapes(img)
        cv2.drawContours( img, other, -1, (255, 255, 0), 1 )
        cv2.drawContours( img, squares, -1, (0, 255, 0), 2 )
        cv2.drawContours( img, circles, -1, (0, 0, 255), 2 )
        cv2.imshow('shapes', img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()
