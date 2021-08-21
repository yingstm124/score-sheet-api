import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def loadImages(file_paths):
    print(file_paths)
    ext = ['png', 'jpg']   
    files = []
    [files.extend(glob.glob(file_paths + '*.' + e)) for e in ext]
    images = [cv2.imread(file) for file in files]
    # print(len(images))
    # for img in images:
    #     showImage(img)

    return images
    

def showImage(img, title=''):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if(title != ''):
        plt.title(title)
    plt.imshow(img)
    plt.show()

def resizeImage(img,width, debug=False):
    height = int(width * img.shape[0]/img.shape[1])
    resize_image  = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
    if(debug):
        showImage(resize_image, 'resized image')
    return resize_image

def resize28Image(img, debug=False,expect_width=22, expect_height=22):
    height = int(img.shape[0])
    width = int(img.shape[1])
    min_ = min(width,height)
    if(width == min_):
        ratio_w = 1
        ratio_h = width*1/height
        new_dimension = ( int(expect_width*ratio_h / ratio_w), expect_width)
    else:
        ratio_w = width*1/height
        ratio_h = 1
        new_dimension = ( expect_width, int(expect_width*ratio_h / ratio_w))        
    img_resize = cv2.resize(img, new_dimension, interpolation=cv2.INTER_AREA)
    w, h = 28, 28
    top_pad = int(np.floor((h - img_resize.shape[0]) / 2).astype(np.uint16))
    bottom_pad = int(np.ceil((h - img_resize.shape[0]) / 2).astype(np.uint16))
    right_pad = int(np.ceil((w - img_resize.shape[1]) / 2).astype(np.uint16))
    left_pad = int(np.floor((w - img_resize.shape[1]) / 2).astype(np.uint16))
    img_resize = np.pad(img_resize, [ (top_pad,bottom_pad) , (left_pad,right_pad) ], "constant", constant_values=0)
    if(debug):
        #print('img size (width, height): ({},{})'.format(width,height))
        #print('ratio : {},{}'.format(ratio_w, ratio_h))
        #print("pad : (top,bottom) , (left,right) = ({},{}), ({},{})".format(top_pad,bottom_pad,left_pad,right_pad))
        showImage(img_resize, 'resized Image')
    return img_resize

# def saveimage(img, img_name, path='output'):
#     path = path + '/' + str(img_name) + '.jpg'
#     cv2.imwrite(path, img)
#     print('save image success !!')

def getAreaByContour(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*peri, True)
    return cv2.boundingRect(approx)

def convertGray2BinaryImage(gray_img):
    bilateral = cv2.bilateralFilter(gray_img, 11, 40, 40)
    blur = gaussiamBlur(bilateral, 5, 5)
    return cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 10)

def convertBgr2GrayImage(rgb_img):
    return cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

def gaussiamBlur(gray_img, filter_width=3, filter_height=3):
    return cv2.GaussianBlur(gray_img,(filter_width,filter_height),0)

def removeNoiseAndShadow(gray_img):
    dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 99)
    diff_img = 255 - cv2.absdiff(gray_img, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return diff_img

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
