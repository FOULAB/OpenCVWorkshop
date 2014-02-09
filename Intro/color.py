"""
color: Opens an image and splits it into color components

Usage: python color.py inputimage
"""

import cv2

def doIt(filename):
   img = cv2.imread(filename)
   if(img == None):
      print "Error: cannot load image " + filename
      return 1

   # Showing the original image
   cv2.namedWindow(filename)
   cv2.imshow(filename, img)   

   for k,planeName in enumerate(['blue', 'green', 'red']):
      cv2.namedWindow(planeName)
      cv2.imshow(planeName, img[:,:,k])
   
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

      return doIt(args[0])

   except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use --help"

   return 2

if __name__ == "__main__":
    sys.exit(main())
