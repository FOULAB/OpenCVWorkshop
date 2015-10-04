import cv
import sys

g_capture=None
g_slider_pos = 0
downUpdateTrackbarPos = False
listenToSlider=False

# this function will be called when the trackbar is updated
def onTrackbarSlide(pos):
   if (listenToSlider):
     downUpdateTrackbarPos = True
     cv.SetCaptureProperty(g_capture, cv.CV_CAP_PROP_POS_FRAMES, pos)
     downUpdateTrackbarPos = False
 
if __name__ == '__main__':
    cv.NamedWindow("Example3", cv.CV_WINDOW_AUTOSIZE)
    if(len(sys.argv)==1):
       g_capture = cv.CaptureFromCAM(0)
       useTrackbar = False
    else:
       g_capture = cv.CreateFileCapture(sys.argv[1])
       useTrackbar = True
       frames = long(cv.GetCaptureProperty(g_capture, cv.CV_CAP_PROP_FRAME_COUNT))
       
       if (frames == 0):
          print "No video"
          loop = False 
       else:
          # create the trackbar and attach the function "onTrackbarSlide" to it
          loop = True
          cv.CreateTrackbar("Position", "Example3", g_slider_pos, frames, onTrackbarSlide)
 
    while(loop):
        if (not ( useTrackbar and downUpdateTrackbarPos) ):
            frame = cv.QueryFrame(g_capture)
            if (frame == None):
               cv.SetTrackbarPos("Position", "Example3", 0)
            cv.ShowImage("Example3", frame)
            # wait until a key is pressed, or 33 ms have passed
            char = cv.WaitKey(33)
            if(useTrackbar):
               # if i dont use the listenToSliderVariable, the act of updating the slide makes it
               # slide, seems like a bug to me.
               listenToSlider=False
               curpos = long(cv.GetCaptureProperty(g_capture, cv.CV_CAP_PROP_POS_FRAMES))
               cv.SetTrackbarPos("Position", "Example3", curpos)
               listenToSlider=True
            # if no key was pressed (timeout) we get -1
            if (char != -1):
                # 27 is esc
                if (char == 27):
                    loop = False
 

