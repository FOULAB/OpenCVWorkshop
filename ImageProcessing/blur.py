"""
Blur: Filter demonstration

Usage: python [-h] blur.py inputimage [outputimage]
"""

import cv2
import numpy as np

def doIt(args):
   img = cv2.imread(args[0])
   if(img == None):
      print "Error: cannot load image " + args[0]
      return 1

   imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert to grayscale
   
   #Simple GaussianBlur, medianBlur and boxFilter examples
   imgFilt = cv2.GaussianBlur(imgGray,(3,3),1)  #sigmaX = 1, sigmaY = 1
   #imgFilt = cv2.medianBlur(imgGray,3)
   #imgFilt = cv2.boxFilter(imgGray,-1,(3,3))  
   
   #Uncomment the following for boxFilter example:
   #cols = imgGray.shape[1]
   #rows = imgGray.shape[0]
   #imgFilt = np.zeros((rows,cols),imgGray.dtype)  #create output image
  # cv2.boxFilter(imgGray,-1,(3,3),imgFilt,(-1,-1),True,cv2.BORDER_REPLICATE)  #all optional parameters used
  
   #Uncomment the following for filter2D example:
   #kernel = (0.1111111)*np.ones((3,3),np.float32)
   #cols = imgGray.shape[1]
   #rows = imgGray.shape[0]
   #imgFilt = np.zeros((rows,cols),imgGray.dtype)  #create output image
   #cv2.filter2D(imgGray,-1,kernel,imgFilt)

   if len(args) > 1:
      cv2.imwrite(args[1], imgFilt)
   else:
      cv2.namedWindow(args[0])
      cv2.imshow(args[0], imgGray)
      cv2.namedWindow("filtered")
      cv2.imshow("filtered", imgFilt)
      cv2.waitKey(0)

   return 0


import sys
import getopt

class Usage(Exception):
   def __init__(self, msg):
      self.msg = msg

def main(argv=None):
   if argv is None:
      argv = sys.argv
    
   try:
      try:
         opts, args = getopt.getopt(argv[1:], "h", ["help"])
      except getopt.error, msg:
         raise Usage(msg)

      # process options
      for o, a in opts:
         if o in ("-h", "--help"):
            print __doc__
            return 0

      # process arguments
      if len(args) < 1:
         print __doc__
         return 0

      return doIt(args)

   except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use --help"

   return 2

if __name__ == "__main__":
    sys.exit(main())
