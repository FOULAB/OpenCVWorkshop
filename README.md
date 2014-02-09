OpenCVWorkshop
==============

Examples for the workshop: Introduction to computer vision with OpenCV held at Foulab
These directories contain examples used in the workshop
Introduction to Computer Vision with OpenCV given at Foulab
Feb 9, 2014 by Rupert Brooks and Isabelle Begin

Some of these examples were taken directly from the OpenCV samples
and copied here for convenience.  Sometimes with small tweaks to
make them work correctly.  The source of this files is indicated
with comments in them.

helloworld.py

To run: python helloworld.py inputimage outputimage

-------------------------------------------------------------------

videograb.py:

To run:  videograb.py deviceNb basename
In window:  "f" key: save frame with basename_0000x.png (x: 0,1,2,...)
	        "escape" key: exit
		
-------------------------------------------------------------------

color.py

To run: color.py inputimage
In window:  any key: exit

-------------------------------------------------------------------

blur.py:

To run: python [-h] blur.py inputimage [outputimage]
In window:  any key: exit

-------------------------------------------------------------------

morphology.py (from openCV samples)

To run: morphology.py inputimage
In window:  "escape" key: exit

-------------------------------------------------------------------

rotating.py

To run: rotating.py
In window: "escape" key: exit

-------------------------------------------------------------------

edge.py (from openCV samples)

To run: edge.py
In window:  "escape" key: exit

-------------------------------------------------------------------

facedetect.py (from openCV samples)

To run: facedetect.py --cascade data\haarcascades\haarcascade_frontal_alt2.xml --nested-cascade data\haarcascades\haarcascade_eye.xml 
In window:  "escape" key: exit

-------------------------------------------------------------------

camshift.py (from openCV samples)

To run: camshift.py 

-------------------------------------------------------------------

plane_ar.py (from openCV samples)
plane_tracker.py (from openCV samples)

-------------------------------------------------------------------

countingchange.py

aTo run: countingchange.py [--method=] [--space=] image

-------------------------------------------------------------------

calibrate.py

To run: calibrate.py --save sonyparameters.npz --debug sonydebug cellphone_calibration/'*'.jpg
 
-------------------------------------------------------------------

features.py

To run: features.py cellphoneseries/DSC_0480_small.jpg cellphoneseries/DSC_0487_small.jpg  test
will generate test.ply which can be viewed by meshlab

-------------------------------------------------------------------

stereo_match.py

To run: stereo_match.py cellphoneseries/DSC_0480_small.jpg cellphoneseries/DSC_0487_small.jpg  test
will generate test.ply which can be viewed by meshlab

-------------------------------------------------------------------

undistortimage.py

To run: undistortimage.py cameraparameterfile inputimage outputimage


