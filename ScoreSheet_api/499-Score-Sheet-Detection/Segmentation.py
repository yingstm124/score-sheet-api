import numpy as np
import cv2
import matplotlib.pyplot as plt

import Utility

class Segmentation:

    def __init__(self, binary_img, debug=False):
        self.debug = debug
        self.binary_image = binary_img
        
    def getSheetBoundary(self, max_cols=20):
        contour_sheet = Utility.contours(self.binary_image, 'RETR_LIST')
        sheet_width = self.binary_image.shape[1]
        cell_minWidth = (sheet_width/max_cols)
        cell_bounding = []
        contour_sheet_sorted, _ = Utility.sortContours(contour_sheet)
        for cnt in contour_sheet_sorted:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if (len(approx) == 4):
                x, y, w, h = cv2.boundingRect(approx)

                if(w > cell_minWidth):
                    cell_bounding.append(self.binary_image[y:y+h, x:x+w])
        
                    if(self.debug):
                        Utility.showImage(self.binary_image[y:y+h, x:x+w],"segment")


        return cell_bounding

    def getID_ScoreBox(self):

        # segment table and score box
        contoursTable = self.contoursExternal(self.binary_image)
        id_table, score_table = self.segmentTable(self.binary_image, contoursTable)
        
        # segment id box
        (contoursBox, _) = self.sort_contours(self.contoursInternal(id_table))
        id_table_num = self.segmentIdbox(id_table, contoursBox)
        
        # segment score box
        (score_table_num, _) = self.sort_contours(self.segmentScoreBox(score_table))

        return id_table_num, score_table_num


    
    def contoursInternal(self, bi_img):
        contours, _ = cv2.findContours(bi_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if(self.debug):
            print("contour Internal")
        
        return contours

    def sort_contours(self, contours, method="left-to-right"):

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

    def resize28Image(self, img, expect_width=22, expect_height=22):

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
        
        return img_resize
    
    def segmentTable(self, bi_img, contours):
        boxlist = []
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if(len(approx) == 4):
                x, y, w, h = cv2.boundingRect(approx)

                if(w > 150):
                    boxlist.append(bi_img[y:y+h, x:x+w])

        id_box = boxlist[0]
        score_box = boxlist[1]
        for box in boxlist:
            if(box.shape[1] > id_box.shape[1]):
                score_box = id_box
                id_box = box
        
        if(self.debug):
            showImage(id_box, 'segment table (student no)')
            showImage(score_box, 'segment table (score)')
        
        return id_box, score_box
    
    def segmentIdbox(self, id_box, contours, c_size=20):
        id_list = []
        i = 0
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if(len(approx) == 4):
                x, y, w, h = cv2.boundingRect(approx)

                if(w > 150 and w < 200):
                    i += 1
                    box = id_box[y+c_size:y+h-c_size, x+20:x+w-c_size]
                    id_list.append(box)

                    if(self.debug):
                        showImage(box,'segment student no width : {}, height : {}'.format(w,h))
        
        digit_list = []

        for id_b in id_list:
            contours = self.contoursExternal(id_b)

            for cnt in contours:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                x, y, w, h = cv2.boundingRect(approx)
                b = id_b[y:y+h, x:x+w]
                b = self.resize28Image(b)
                digit_list.append(b)

                if(self.debug):
                    print("approx : {}, {}".format(len(approx), approx))
                    showImage(b, 'resize image 28 pixel')

        return digit_list

    def segmentScoreBox(self, score_box, c_size=30):

        score_box = score_box[+c_size:-c_size, +c_size:-c_size]
        contours, _ = cv2.findContours(score_box, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        score_list = []

        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            #print("approx : {}, {}".format(len(approx), approx))

            x, y, w, h = cv2.boundingRect(approx)

            b = score_box[y:y+h, x:x+w]

            if(self.debug):
                showImage(b,'Segment score ({},{})'.format(b.shape[0], b.shape[1]))

            if(h > 20 and h < score_box.shape[0] and w < score_box.shape[1]):
                
                b = self.resize28Image(b)
                score_list.append(b)

                if(self.debug):
                    showImage(b,'score box ({},{})'.format(b.shape[0], b.shape[1]))

        return score_list



