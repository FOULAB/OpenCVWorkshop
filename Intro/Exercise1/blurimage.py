import cv
import sys

if(len(sys.argv)==1):
   print "Usage: blurimage.py inputimage outputimage"
else:
   myimage=cv.LoadImage(sys.argv[1])
   filteredimage = cv.CreateImage(cv.GetSize(myimage),myimage.depth, myimage.nChannels)
   #cv.Smooth(myimage,filteredimage,cv.CV_BILATERAL,21,0,2,5) #wierd... cant get it to work
   cv.Smooth(myimage,filteredimage,cv.CV_GAUSSIAN,7)
   # try me instead and see...
   #filteredimage = cv.CreateImage(cv.GetSize(myimage),cv.IPL_DEPTH_16S, myimage.nChannels)
   #cv.Laplace(myimage,filteredimage,7)

   if len(sys.argv)>2:
      cv.SaveImage(sys.argv[2],filteredimage)
   else:
      cv.NamedWindow(sys.argv[1])
      cv.ShowImage(sys.argv[1],filteredimage)
      cv.WaitKey(0)

