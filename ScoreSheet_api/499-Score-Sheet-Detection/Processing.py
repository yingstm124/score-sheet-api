import cv2
from matplotlib.pyplot import contour
import numpy as np
import Utility


def get_adaptive_binary_image(rgb_image,debug=False):
    # 1. convert gray image
    gray_img = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    if (debug):
        Utility.showImage(gray_img,'gray image')
        
    # 2. remove shadow
    dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 99)
    diff_img = 255 - cv2.absdiff(gray_img, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    if(debug):
        Utility.showImage(diff_img, 'remove shadow')

    # 3. convert 1-channel image (binary image)
    bilateral = cv2.bilateralFilter(gray_img, 11, 40, 40)
    blur = cv2.GaussianBlur(bilateral,(5,5),0)
    thresh_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 10)

    if(debug):
        # Utility.showImage(bilateral, 'bilateral image')
        # Utility.showImage(blur, 'blur')
        Utility.showImage(thresh_img, 'thresholding (binary image)')
        
    return thresh_img



def contours(binary_image, mode="RETR_EXTERNAL"):
    if mode == "RETR_EXTERNAL":
        contours, _ = cv2.findContours(binary_image , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    elif mode == "RETR_LIST":
        contours, _ = cv2.findContours(binary_image , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
    return contours, _


def sortContours(contours, method="left-to-right", debug=False):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
            
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    
    (cnts_, boundingBoxes_) = zip(*sorted(zip(contours, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
            
    return (cnts_, boundingBoxes_)

