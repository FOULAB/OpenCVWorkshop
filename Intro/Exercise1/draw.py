#This is Isabelle's comment OMGPONIES but ponies don't like pythons. Nope.

import cv2
import sys
#def print_image_type( t ):
#   if t==cv2.IPL_DEPTH_8U:
#      print("Unsigned 8-bit integer")
#   elif t==cv2.IPL_DEPTH_8S:
#      print("Signed 8-bit integer")
#   elif t==cv2.IPL_DEPTH_16U:
#      print("Unsigned 16-bit integer")
#   elif t==cv2.IPL_DEPTH_16S:
#      print("Signed 16-bit integer")
#   elif t==cv2.IPL_DEPTH_32S:
#      print("Signed 32-bit integer")
#   elif t==cv2.IPL_DEPTH_32F:
#      print("Single-precision floating point")
#   elif t==cv2.IPL_DEPTH_64F:
#      print("Double-precision floating point")
#   else:
#      print("Unknown type")


if(len(sys.argv)==1):
   print "Usage: Helloworld.py inputimage {outputimage}"
   print ""
   print "Will either display the image, or resave it under a new name"
else:
   myimage=cv2.imread(sys.argv[1])
   print "Width: %d Height %d Channels: %d " %  myimage.shape
   #print_image_type( myimage.depth )
   cv2.line(myimage,(0,0),(myimage.shape[0],myimage.shape[1]),(255,0,255),2)
   
 
#  if len(sys.argv)>2:
#      cv.SaveImage(sys.argv[2],myimage)
#   else:
   cv2.imshow(sys.argv[1],myimage)
   cv2.waitKey()

