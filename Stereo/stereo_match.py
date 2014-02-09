#/usr/bin/env python
# copied from openCV 2.4.6 examples
'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

import numpy as np
import cv2
import sys

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')


    
def stereo_process(imgL,imgR,outprefix):
    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp
    stereo = cv2.StereoSGBM(minDisparity = min_disp,
        numDisparities = num_disp,
        SADWindowSize = window_size,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32,
        disp12MaxDiff = 1,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        fullDP = False
    )

    print 'computing disparity...'
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    print 'generating 3d point cloud...',
    h, w = imgL.shape[:2]
    f = 0.8*w                          # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    if(outprefix):
       out_fn = outprefix+'.ply'
       write_ply(out_fn, out_points, out_colors)
       print '%s saved' % out_fn

    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp-min_disp)/num_disp)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if(len(sys.argv)<3):
       print "Usage: stereo_match leftimage rightimage {outprefix}"
    else:
       print 'loading images...'
       imgL = cv2.pyrDown( cv2.imread(sys.argv[1]) )  # downscale images for faster processing
       imgR = cv2.pyrDown( cv2.imread(sys.argv[2]) )
       if(len(sys.argv)>=4):
          stereo_process(imgL,imgR,sys.argv[3])
       else:
          stereo_process(imgL,imgR,None)

