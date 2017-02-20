import cv2
import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import imghdr


class camera:
    """
    a camera model to be undistorted
    and undistort any image taken by this camera
    """

    def __init__(self, path, nx, ny, out_path = None, draw = False):
        """
        get all the image points for camera calibration out of a group of images

        params:
            - path: the folder contains chessborads
            - nx: integer, specify how many itersections horizontally
              on the chessborads
            - ny: same as nx, except it's vertically
            - out_path: the path to store chessborads with corners drew
            - draw: bool, whether to save the images with corners

        return:
            - tuple of lists:
              object points, image_points
        """
        self.nx = nx
        self.ny = ny
        self.img_paths = []
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if imghdr.what(img):
                self.img_paths.append(img)

        objp = np.zeros((ny*nx,3), np.float32)
        objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
        objpoints = []
        imgpoints = []

        for i, filename in enumerate(self.img_paths):
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)
                if draw:
                    cv2.drawChessboardCorners(img, (nx,ny), corners, ret)
                    write_path = os.path.join(out_path, ("%d_with_corners.jpg"%(i+1)))
                    cv2.imwrite(write_path, img)

        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(
                                   objpoints, imgpoints, gray.shape[::-1],None,None)




    def cal_undist(self, img = None):
        """
        calulate a undistorted version of a image based on the camera model

        params:
            - imgs: images (numpy array)
        return:
            - image
        """
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
