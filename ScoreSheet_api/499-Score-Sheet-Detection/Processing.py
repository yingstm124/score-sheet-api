import sys 
import cv2
import numpy as np
from numpy.lib.type_check import imag
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
    elif mode == "RETR_TREE":
        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
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

def fourCornersSort(pts):
    diff = np.diff(pts, axis=1)
    summ = pts.sum(axis=1)
    return np.array([pts[np.argmin(summ)],
                     pts[np.argmax(diff)],
                     pts[np.argmax(summ)],
                     pts[np.argmin(diff)]])


def contourOffset(cnt, offset):

    cnt += offset
    cnt[cnt < 0] = 0
    return cnt

def biggerCountour(contours):
    biggest = np.array([])
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area

def reOrder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    
    diff =np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    
    return myPointsNew

def getPerspective(image, bi_img, debug=False):
        
    contours, _ = cv2.findContours(bi_img , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest, maxArea = biggerCountour(contours)
    heightImg, widthImg  = 500,800
    
    
    if biggest.size != 0:
        _, _, w, h = cv2.boundingRect(biggest)
        widthImg = w
        heightImg = h
        # widthImg = biggest[0][len(biggest)-1][1] - biggest[0][0][1]
        # heightImg = biggest[0][len(biggest)-1][0] - biggest[0][0][0]
        
        if(debug):
            print("{0} : {1}".format(widthImg,heightImg))
            
        biggest = reOrder(biggest) 
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        imgWrapColored = cv2.warpPerspective(bi_img, matrix, (widthImg, heightImg))
    
    if(debug):
        cv2.drawContours(image, biggest, -1, (0,255,0), 100)
        Utility.showImage(image, 'contour image')
        Utility.showImage(imgWrapColored, 'imgWrapColored')
        
    return imgWrapColored

