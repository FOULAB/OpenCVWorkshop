'''
Compares two images, use spacebar to flip between them

usage: imagecompare.py image1 image2

SPACE - change which image
ESC   - exit

Feb 2014 - example by Rupert Brooks
'''

import sys
import cv2

def imagecompare():
   if(len(sys.argv)!=3):
      print __doc__
      return;
   try:
      image0 = cv2.imread(sys.argv[1])
   except IOError:
      print "Error: cannot load image " + sys.argv[1]
      return;
   try:
      image1 = cv2.imread(sys.argv[2])
   except IOError:
      print "Error: cannot load image " + sys.argv[2]
      return;
   face=cv2.FONT_HERSHEY_PLAIN
   fontscale=1.5
   thick=2
   cv2.putText(image0,sys.argv[1],(30,30),face,fontscale,(255,0,255), thick)
   cv2.putText(image1,sys.argv[2],(30,30),face,fontscale,(255,0,255), thick)


   state=0
   cv2.namedWindow("comparing")
   cv2.imshow("comparing", image0)
   while(True):

      theKey=cv2.waitKey(0)
      if(theKey==27):
         break;
      elif(theKey==ord(' ')):
         state=1-state
         if(state==0):
            cv2.imshow("comparing",image0)
         else:
            cv2.imshow("comparing",image1)




if __name__ == '__main__':
 imagecompare()
