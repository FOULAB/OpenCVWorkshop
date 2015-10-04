import cv2
import sys

# This script plays video from the camera, and grabs frames into images
# frame 00000, frame 00001, etc
# note that it will overwrite the frames captured before.
#
# for a more sophisticated example, see the video.py example in the openCV 
# examples
 
if __name__ == '__main__':
    framecounter = 0
    cv2.namedWindow("grabby")
    videodevice=0
    if(len(sys.argv)>1):
      videodevice=int(sys.argv[1])
    g_capture = cv2.VideoCapture(videodevice)
    if g_capture is None or not g_capture.isOpened():
        print 'Warning: unable to open video source: ', source
    ret = False
    loop = True
    while(not ret):
       ret,frame = g_capture.read()
    basename="frame_"
    if(len(sys.argv)>2):
      basename=sys.argv[2]
    while(loop):
       ret, frame = g_capture.read()
       if not ret:
          print "No frame acquired"
          break;

       cv2.imshow("grabby", frame)
       char = cv2.waitKey(33)
       if (char != -1):
          # key 102 is lowercase f
          if(char == 102):
             framename=basename + ("%05d.png" % framecounter)
             print "Saving "+framename
             framecounter=framecounter+1
             cv2.imwrite(framename,frame)
          elif (char == 27):
             loop = False
 

