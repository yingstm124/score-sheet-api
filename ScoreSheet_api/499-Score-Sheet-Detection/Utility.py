import cv2
import matplotlib.pyplot as plt
import numpy as np

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


def resize28Image(img, debug=False,expect_width=28, expect_height=28):

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


def get_bounding_rect_content(img, bounding_rect):
    x, y, w, h = bounding_rect
    return img[y:y+h, x:x+w]


# def saveimage(img, img_name, path='output'):
#     path = path + '/' + str(img_name) + '.jpg'
#     cv2.imwrite(path, img)
#     print('save image success !!')