
'''
This example plays video from the camera, and finds features
using different feature detection methods.

Usage features.py [videosource]

while running use the following keys
b - BRISK detector
o - ORB detector
s - SIFT detector
u - SURF detector

a - toggle showing all, or first 50
d - toggle showing the first descriptor that is returned

ESC - exit

Feb 2014 - Example by Rupert Brooks
'''
import cv2
import sys

def drawLeftText(img,ctr,text):
   face=cv2.FONT_HERSHEY_PLAIN
   fontscale=1.5
   thick=2
   sz,baseline=cv2.getTextSize(text,face,fontscale,thick)
   cv2.putText(img,text,(int(ctr[0]),int(ctr[1])),face,fontscale,(255,0,255), thick)


if __name__ == '__main__':
    print __doc__
    framecounter = 0
    cv2.namedWindow("Features")
    videodevice=0
    if(len(sys.argv)>1):
      videodevice=int(sys.argv[1])

    g_capture = cv2.VideoCapture(videodevice)
    if g_capture is None or not g_capture.isOpened():
        print 'Warning: unable to open video source: ', source
    loop = True
    basename="frame_"
    if(len(sys.argv)>2):
      basename=sys.argv[2]

    currentState=""
    nextState="ORB"
    showDescriptor=False
    drawAll=False
    while(loop):
       if(currentState != nextState):
          if(nextState == "ORB"):
              detector=cv2.ORB( )
              currentState=nextState
          elif(nextState == "BRISK"):
              detector=cv2.BRISK()
              currentState=nextState
          elif(nextState == "SIFT"):
              detector=cv2.SIFT()
              currentState=nextState
          elif(nextState == "SURF"):
              detector=cv2.SURF()
              currentState=nextState
          else:
              print "Unknown state", nextState
              nextState=currentState
       ret, frame = g_capture.read()
       if not ret:
          print "No frame acquired"
          break;
       keypoints,descriptors = detector.detectAndCompute(frame, None)
       if(not drawAll and len(keypoints) > 50):
           keypoints=keypoints[:50]

       result=cv2.drawKeypoints(frame,keypoints,flags=4)
       drawLeftText(result,(10,30),currentState)
       if(showDescriptor):
          if(descriptors != None and len(descriptors)>0):
             print "First descriptor:",descriptors[0]

       cv2.imshow("Features", result)
       char = cv2.waitKey(33)
       if(char == 27):
            break;
       elif(char == ord('o')):
            nextState="ORB"
            print "ORB detector"
       elif(char == ord('b')):
            nextState="BRISK"
            print "BRISK detector"
       elif(char == ord('s')):
            nextState="SIFT"
            print "SIFT detector"
       elif(char == ord('u')):
            nextState="SURF"
            print "SURF detector"
       elif(char == ord('a')):
           drawAll=not drawAll
       elif(char == ord('d')):
           showDescriptor=not showDescriptor
 

