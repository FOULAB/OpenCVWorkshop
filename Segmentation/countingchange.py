#/usr/bin/env python
'''
Segmentation example.

Sample shows a semi-serious machine vision example for counting
change, which segments coins, and a calibration object to determine size, 
and then tries to count the amount of money present.

Usage:
  segment.py  [--method X] [--space Y]
      [<input image>]

  Use sliders to adjust parameters.
  Keys:
    ESC   - exit
    i     - show the input image
    space - show, or not the shapes found
    s     - show, or not the segmentation

  method is otsu, threshold, adaptive
  space is hue, grey

  Feb 2014 Original example R. Brooks

'''

import numpy as np
import cv2
import math
bins = np.arange(256).reshape(256,1)

# from example hist.py
def hist_curve(im):
    h = np.zeros((300,256,3),dtype='uint8')
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins,hist)))
        cv2.polylines(h,[pts],False,col)
    y=np.flipud(h).copy()
    return y

# from example squares.py
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

# based on example shapes.py
def find_shapes(img):
    squares = []
    circles = []
    other = []
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        area=cv2.contourArea(cnt)
        if(area>=1000):
           pass
           #print "Contour:",len(cnt),cnt_len,area,abs(cnt_len/math.sqrt(area) -2*math.sqrt(math.pi))
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

def drawLeftText(img,ctr,text):
   face=cv2.FONT_HERSHEY_PLAIN
   fontscale=1.5
   thick=2
   sz,baseline=cv2.getTextSize(text,face,fontscale,thick)
   cv2.putText(img,text,(int(ctr[0]),int(ctr[1])),face,fontscale,(255,0,255), thick)

def drawCenteredText(img,ctr,text):
   face=cv2.FONT_HERSHEY_PLAIN
   fontscale=1.5
   thick=2
   sz,baseline=cv2.getTextSize(text,face,fontscale,thick)
   cv2.putText(img,text,(int(ctr[0]-sz[0]/2),int(ctr[1]+sz[1]/2)),face,fontscale,(255,0,255), thick)

def countingchange(opts,args):
    if (len(args)==0):
       return
    method=opts.get('--method','otsu').lower()
    space =opts.get('--space','grey').lower()
    print "Using Method:",method
    fn = args[0]

    img = cv2.imread(fn)
    if("grey"==space):
       greyimage=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
       inputimage=greyimage
    elif("hue"==space):
       hsvimage=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
       hueimage=hsvimage[:,:,0]
       inputimage=hueimage
    else:
       print "Unknown image space:",space
       raise Exception("Unknown image space:",space)

    win="Segmentation"
    
    cv2.namedWindow(win)
    drawingState="INPUT"
    def computeRadius(cnt,scale):
      center,radius=cv2.minEnclosingCircle(cnt)
      return radius*scale
	
    def computeCenter(cnt):
      center,radius=cv2.minEnclosingCircle(cnt)
      return center 

    def identifyCoin(radius):
       #19mm 9.5  penny
       #17.9mm 8.95 dime
       #23.9 11.95 quarter
       #26.4 13.2 loon
       #21.1 10.5 nickel
       #27.9  14 twonie
       if(9.25 < radius and 9.75 > radius):
          return "penny"
       if(10.1 <  radius and 10.9 > radius):
          return "nickel"
       if(8.5 < radius and 9.25 > radius):
          return "dime"
       if(11.5 < radius and 12.5 > radius):
          return "quarter"
       if(12.8 < radius and 13.5 > radius):
          return "loonie"
       if(13.5 < radius and 14.5 > radius):
          return "twonie"
       return "???"
    def computeValue(coin):
        if(coin == "penny"):
           return 0.01
        if(coin == "nickel"):
           return 0.05
        if(coin == "dime"):
           return 0.10
        if(coin == "quarter"):
           return 0.25
        if(coin == "loonie"):
           return 1.00
        if(coin == "twonie"):
           return 2.00
        return 0

    def findCoins(squares,circles):
       if(len(squares)==0):
          return "Not Enough Squares",["?"]*len(circles),"?"
       if(len(squares)>1):
          return "Too Many Squares",["?"]*len(circles),"?"
       scale=80.0/cv2.arcLength(squares[0],True)
       circleText=[identifyCoin(computeRadius(circle,scale)) for circle in circles]
       print "Circle Text",circleText
       print map(computeValue,circleText)
       return "Success",circleText,"$%0.2f"%reduce(lambda x,y:x+y,map(computeValue,circleText),0)

        

    def findAndDrawShapes(segmentation):
       dispimg=img.copy()
       zeColors=np.asarray([(255,0,0),(0,255,0)])
       overlay=zeColors[np.minimum(segmentation,1)]
       dispimg=cv2.addWeighted(dispimg,0.8,overlay,0.2,.0,dtype=cv2.CV_8UC3)
       squares,circles,other = find_shapes(segmentation)
       result,circleText,value=findCoins(squares,circles)
       circleCentres=[computeCenter(circle) for circle in circles]
       drawLeftText(dispimg,(100,50),result)
       for i in range(len(circleCentres)):
          drawCenteredText(dispimg,circleCentres[i],circleText[i])
       drawLeftText(dispimg,(dispimg.shape[1]-100,50),value)

       cv2.drawContours( dispimg, other, -1, (255, 255, 0), 1 )
       cv2.drawContours( dispimg, squares, -1, (0, 255, 0), 2 )
       cv2.drawContours( dispimg, circles, -1, (0, 0, 255), 2 )
       cv2.imshow(win,dispimg)  #result)

    if 'otsu' == method:
       (thresh,result)=cv2.threshold(inputimage,0,255,cv2.THRESH_OTSU)
       curve=hist_curve(inputimage)
       cv2.line(curve,(int(thresh),0),(int(thresh),299),(255,0,255),2)
       cv2.imshow('histogram',curve)
       def update(_):
          if drawingState == "INPUT":
             cv2.imshow(win,inputimage)
          elif drawingState == "SEGMENTATION":
             cv2.imshow(win,result)
          elif drawingState == "SHAPES":
             findAndDrawShapes(result)
          else:
             cv2.imshow(win,result)  #result)
    elif 'threshold' == method:
       def update(_):
          threshval=cv2.getTrackbarPos('Threshold Level',win)
          (thresh,result)=cv2.threshold(inputimage,threshval,255,cv2.THRESH_BINARY)
          curve=hist_curve(inputimage)
          cv2.line(curve,(int(thresh),0),(int(thresh),299),(255,0,255),2)
          cv2.imshow('histogram',curve)
          if drawingState == "INPUT":
             cv2.imshow(win,inputimage)
          elif drawingState == "SEGMENTATION":
             cv2.imshow(win,result)
          elif drawingState == "SHAPES":
             findAndDrawShapes(result)
          else:
             cv2.imshow(win,result)  #result)
       cv2.createTrackbar('Threshold Level', win, 128, 255, update)
       update(None)
    elif 'adaptive' == method:
       def update(_):
          bias=cv2.getTrackbarPos('Bias',win)-10
          print "Bias:",bias
          blocksize=cv2.getTrackbarPos('Block Size',win)*2+3
          print "blocksize:",blocksize
          result=cv2.adaptiveThreshold(inputimage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blocksize,bias)
          if drawingState == "INPUT":
             cv2.imshow(win,inputimage)
          elif drawingState == "SEGMENTATION":
             cv2.imshow(win,result)
          elif drawingState == "SHAPES":
             findAndDrawShapes(result)
          else:
             cv2.imshow(win,result)  #result)
       cv2.createTrackbar('Block Size', win, 0, 10, update)
       cv2.createTrackbar('Bias', win, 10, 20, update)
       update(None)
    else:
        raise Exception("Unknown method:",method)

    while True:
        ch = cv2.waitKey()
        if ch == ord(' '):
            drawingState="SHAPES"
            update(None)
        if ch == ord('i'):
            drawingState="INPUT"
            update(None)
        if ch == ord('s'):
            drawingState="SEGMENTATION"
            update(None)
        if ch == 27:
            break
 
if __name__ == '__main__':
    print __doc__
    import sys
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], '', ['method=','space='])
    opts = dict(opts)
    print opts
    try:
       countingchange(opts,args)
    except:
       print "counting change failed:",sys.exc_info()[0]
    
