import cv2
import sys
import numpy
# Example by Rupert Brooks, 2014

if(len(sys.argv)<3):
   print "Usage: undistort.py cameraparameters inputimage {outputimage}"
else:
   camerafile=numpy.load(sys.argv[1])
   print "Camera intrinsic parameters"
   print camerafile['camera_matrix']
   print "Camera distortion parameters"
   print camerafile['distortion_parameters']
 
   imgIn=cv2.imread(sys.argv[2])
   imgUn=cv2.undistort(imgIn, camerafile['camera_matrix'], camerafile['distortion_parameters']) 

   if len(sys.argv)>3:
      cv2.imwrite(sys.argv[3],imgUn)
   else:
      cv2.imshow(sys.argv[2],imgUn)
      cv2.waitKey()

