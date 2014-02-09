"""
HelloWorld: First demonstration of OpenCV

Usage: Helloworld.py inputimage outputimage
"""

import cv2


def helloWorld(args):
   myimage = cv2.imread(args[0],cv2.CV_LOAD_IMAGE_UNCHANGED)
   if(myimage == None):
         print "Error: cannot load image " + args[0]
         return 1

   print "Type of myimage",type(myimage)
   if len(myimage.shape)>2:
      channels =  myimage.shape[2]
   else:
      channels = 1
   print "Width: %d Height %d Channels: %d " % ( myimage.shape[1], myimage.shape[0], channels)
   print "Image data type: ", myimage.dtype 

   if len(args) > 1:
      cv2.imwrite(args[1], myimage)
   else:
      cv2.namedWindow(args[0])
      cv2.imshow(args[0], myimage)
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

      return helloWorld(args)

   except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use --help"

   return 2

if __name__ == "__main__":
    sys.exit(main())
