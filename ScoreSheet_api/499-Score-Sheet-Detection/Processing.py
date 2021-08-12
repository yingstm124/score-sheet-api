import cv2
import numpy as np
import math
import Utility


# class BinaryImage:

#     def __init__(self, image, debug=False):
#         self.debug = debug
#         self.rgb_image = image

#     def getBinaryImage(self):
#         # 1. convert gray image
#         gray_img = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2GRAY)
#         if (self.debug):
#             Utility.showImage(gray_img,'gray image')
        
#         # 2. remove shadow
#         dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
#         bg_img = cv2.medianBlur(dilated_img, 99)
#         diff_img = 255 - cv2.absdiff(gray_img, bg_img)
#         norm_img = diff_img.copy()
#         cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
#         if(self.debug):
#             Utility.showImage(diff_img, 'remove shadow')

#         # 3. convert 1-channel image (binary image)
#         bilateral = cv2.bilateralFilter(gray_img, 11, 40, 40)
#         blur = cv2.GaussianBlur(bilateral,(5,5),0)
#         thresh_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 10)

#         if(self.debug):
#             # Utility.showImage(bilateral, 'bilateral image')
#             # Utility.showImage(blur, 'blur')
#             Utility.showImage(thresh_img, 'thresholding (binary image)')
        
#         return  thresh_img


class CellSheets:

    def __init__(self, img, binaryImage, debug=False, max_cols=20):
        self.debug = debug
        self.original_image = img
        self.binary_image = binaryImage  
        self.min_width_cell =  self.binary_image.shape[1]/max_cols
        self.max_cols = max_cols    

    def processing(self):
        ''' 
            - POC Issue sorted contours -

            [/] 1. get external cell by using external contouring
            [/] 2. get rows by using contouring
            [ ] 3. order row and colum of cell
            [ ] 4. predict & mapping data structure 
                    : identify three part
                        - Text
                        - Number Text
                        - Handwritten (Model)
        '''
        datas = dict()
        contours, _ = Utility.contours(self.binary_image)
        binary_external_cell, rgb_external_cell = self.getExternalCell(contours)
        external_cell_rows = self.boundingRows(binary_external_cell, rgb_external_cell)

        if(self.debug):
            Utility.showImage(self.binary_image, "orginal binary image")
            Utility.showImage(binary_external_cell, "number of row : {0}".format(len(external_cell_rows)-1))
            Utility.showImage(rgb_external_cell, "number of row : {0}".format(len(external_cell_rows)-1))

        return datas

    def isSquareBox(self, approx):
        return len(approx) == 4

    def isCellBox(self, approx, width):
        return len(approx) == 4 and (width > self.min_width_cell)
    
    def getExternalCell(self, contours, buffer=0):
        binary_external_cells = []
        rgb_external_cells = []
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            if(self.isSquareBox(approx) and self.isCellBox(approx,w)):    
                bi_img = self.binary_image[y-buffer:y+h+buffer, x-buffer:x+w+buffer]
                rgb_img = self.original_image[y-buffer:y+h+buffer, x-buffer:x+w+buffer]
                binary_external_cells.append(bi_img)
                rgb_external_cells.append(rgb_img)
        
        return binary_external_cells[0], rgb_external_cells[0]

    def boundingRows(self, binary_img, rgb_img):
        # Detect horizontal lines
        result = rgb_img.copy()
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        detect_horizontal = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        contours, _ = Utility.contours(detect_horizontal)
        contours, _ = Utility.sortContours(contours,method="top-to-bottom")
        i = 0
        _, pre_y, _, _ = Utility.getAreaByContour(contours[0])
        rows = []
        for c in contours:
            x, y, _, _ = Utility.getAreaByContour(c)
            print(y)
            if(i > 0):
                start_pox_y = pre_y
                end_pos_y = y
                row = rgb_img[start_pox_y:end_pos_y,:]
                if(self.debug):
                    Utility.showImage(row, "row {0}".format(i))
                rows.append(row)
            if(self.debug):
                cv2.putText(result, "{0}".format(i), (x,y),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),2,cv2.LINE_AA)
                cv2.drawContours(result, [c], -1, (36,255,12), 2)
            i += 1
            pre_y = y

        if(self.debug):
            Utility.showImage(result)
        
        return rows

    





    