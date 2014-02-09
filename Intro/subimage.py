"""
Subimage: Demonstration of drawing into a subregion / roi
          Demonstration of how numpy has more versatile memory layout
          than open cv

          In regular python lists
          A=B  is a reference
          A=B[:] makes a copy
   
          This is not generally true with Numpy arrays (openCV)
          In general,  
          A=B, or A=B[:] is a view
          but "fancy indexing" makes a copy
          a copy can be forced with A=B.copy()
          http://stackoverflow.com/questions/4370745/view-onto-a-numpy-array

          Numpy supports very versatile views into arrays, to avoid memory 
          copying unnecessarily.  Numpy is more versatile than openCV, and
          openCV will complain if the numpy memory layout cannot be imitated
          with a CV::Mat

Usage: subimage.py inputimage
"""

import cv2
import numpy


def subimage(args):
   try:
      myimage = cv2.imread(args[0])
   except IOError:
      print "Error: cannot load image " + args[0]
      return 1

   if len(myimage.shape)>2:
      channels =  myimage.shape[2]
   else:
      channels = 1

   # make a copy to go back to the original later
   myimagecopy=myimage.copy()


   # show original image
   cv2.namedWindow("original image")
   cv2.imshow("original image", myimage)
   cv2.waitKey(0)
   cv2.destroyWindow("original image")

   # lets create a sub image in the middle
   rows=myimage.shape[0]
   cols=myimage.shape[1]
   r1=rows//3
   r2=2*rows//3
   c1=cols//3
   c2=2*cols//3
   mysubimage=myimage[r1:r2,c1:c2,:]
   cv2.namedWindow("subimage")
   cv2.imshow("subimage", mysubimage)
   cv2.waitKey(0)
   cv2.destroyWindow("subimage")
   
   # lets blur that sub image IN PLACE
   # and then look at the original image
   # this shows that the subimage is just a view
   # onto the same memory as the original
   cv2.GaussianBlur(mysubimage,(0,0),5,mysubimage)
   
   cv2.namedWindow("blur roi")
   cv2.imshow("blur roi", myimage)
   cv2.waitKey(0)
   cv2.destroyWindow("blur roi")

   # go back to clean original image
   myimage=myimagecopy.copy()
   # take a sub image of every other pixel
   mysubimage=myimage[::2,::2,:]
   cv2.namedWindow("subimage")
   cv2.imshow("subimage", mysubimage)
   cv2.waitKey(0)
   cv2.destroyWindow("subimage")
   
   # try to blur that sub image
   # this will fail - open CV does not support that memory layout
   cv2.GaussianBlur(mysubimage,(0,0),5,mysubimage)
   
   cv2.namedWindow("blur roi")
   cv2.imshow("blur roi", myimage)
   cv2.waitKey(0)
   cv2.destroyWindow("blur roi")
   

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

      return subimage(args)

   except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use --help"

   return 2

if __name__ == "__main__":
    sys.exit(main())
