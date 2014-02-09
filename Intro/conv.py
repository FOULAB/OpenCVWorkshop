""" Blur: Filter demonstration

Usage: python [-h] blur.py inputimage [outputimage]
"""

import cv
import numpy

def doIt(args):
   try:
      img = cv.LoadImage(args[0])
   except IOError:
      print "Error: cannot load image " + args[0]
      return 1

   imgGray = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
   cv.CvtColor(img, imgGray, cv.CV_RGB2GRAY)
   
   imgFilt = cv.CreateImage(cv.GetSize(imgGray), cv.IPL_DEPTH_8U, 1)
   
   kernel = cv.CreateMat(3, 3, cv.CV_32F)
   for r in xrange(3):
      for c in xrange(3):
         kernel[r,c] = 1./9.
##   kernel[0,0] = 1
##   kernel[0,1] = 1
##   kernel[0,2] = 1
##   kernel[1,0] = 1
##   kernel[1,1] = 1
##   kernel[1,2] = 1
##   kernel[2,0] = 1
##   kernel[2,1] = 1
##   kernel[2,2] = 1
   
   #kernel = numpy.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]])
   cv.Filter2D(imgGray, imgFilt, kernel)
   
   if len(args) > 1:
      cv.SaveImage(args[1], imgFilt)
   else:
      cv.NamedWindow(args[0])
      cv.ShowImage(args[0], imgGray)
      cv.NamedWindow("filtered")
      cv.ShowImage("filtered", imgFilt)
      cv.WaitKey(0)

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
