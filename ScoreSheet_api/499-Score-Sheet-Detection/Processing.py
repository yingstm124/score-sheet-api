import cv2
import numpy as np
import Utility

def contours(binary_image, mode="RETR_EXTERNAL"):
    if mode == "RETR_EXTERNAL":
        contours, _ = cv2.findContours(binary_image , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    elif mode == "RETR_LIST":
        contours, _ = cv2.findContours(binary_image , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
    return contours

def sortContours(contours, method="left-to-right", debug=False):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
            
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (cnts, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
            
    return (cnts, boundingBoxes)