import cv2
import numpy as np

import Utility
import Processing


class BinaryImage:

    def __init__(self, image, debug=False):
        self.debug = debug
        self.rgb_image = image

    def getBinaryImage(self):
        # 1. convert gray image
        gray_img = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2GRAY)
        if (self.debug):
            Utility.showImage(gray_img,'gray image')
        
        # 2. remove shadow
        dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 99)
        diff_img = 255 - cv2.absdiff(gray_img, bg_img)
        norm_img = diff_img.copy()
        cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        if(self.debug):
            Utility.showImage(diff_img, 'remove shadow')

        # 3. convert 1-channel image (binary image)
        bilateral = cv2.bilateralFilter(gray_img, 11, 40, 40)
        blur = cv2.GaussianBlur(bilateral,(5,5),0)
        thresh_img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 35, 10)

        if(self.debug):
            # Utility.showImage(bilateral, 'bilateral image')
            # Utility.showImage(blur, 'blur')
            Utility.showImage(thresh_img, 'thresholding (binary image)')
        
        return  thresh_img


class CellSheets:

    def __init__(self, img, binaryImage, debug=False, max_cols=20):
        self.debug = debug
        self.orginalImage = img
        self.binary_image = binaryImage  
        self.max_cols = max_cols    
        self.amountOfRow = 0
        self.paper = np.zeros(img.shape, dtype=np.uint8)

    def getCellSheets(self):

        # 1. contour all for finding cell            
        contour_sheet, _ = Processing.contours(self.binary_image, 'RETR_LIST')
            
        # 2. sorting contour
        contour_sheet_sorted, _ = Processing.sortContours(contour_sheet, method="left-to-right", debug=self.debug)

        # 3. add cell image in cell bounding array
        sheet_width = self.binary_image.shape[1]
        cell_minWidth = (sheet_width/self.max_cols)
        row_cell = []
        digit_cell = []
        student_id_cell = []
        temp_cell = []
        i = 0
        amount_of_row = 0
        first_row_width = 0
        for cnt in contour_sheet_sorted:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if (len(approx) == 4):
                x, y, w, h = cv2.boundingRect(approx)

                is_digit_cell = True if w/h < 2 else False
                if(w > cell_minWidth):
                    temp_cell.append(self.binary_image[y:y+h, x:x+w])

                    if(is_digit_cell):
                        cell_ = self.binary_image[y+10:y+h-10, x+10:x+w-10]
                        digit_cell.append(cell_)
                        
                        if(self.debug):
                            Utility.showImage(cell_, 'box')
                            
                        digit_contours, _ = Processing.contours(cell_)
                        digit_contours_sorted, _ = Processing.sortContours(digit_contours)
                        
                        for dc in digit_contours_sorted:
                            peri_ = cv2.arcLength(dc, True)
                            approx_ = cv2.approxPolyDP(dc, 0.02 * peri_, True)
                            x_, y_, w_, h_ = cv2.boundingRect(approx_)
                            
                            d_cell_ = cell_[y_:y_+h_,x_:x_+w_]
                            if(self.debug):
                                Utility.showImage(d_cell_, '{0},{1}'.format(w_,h_))
                            
                        # if(self.debug):
                        #     Utility.showImage(self.binary_image[y:y+h, x:x+w],"digit cell (width,height) : ({0},{1})".format(w,h))

                    if(i == 1): 
                        first_row_width = w
                    
                    if(w >= first_row_width-100 and w <= first_row_width+100 and first_row_width > 0):
                        amount_of_row = amount_of_row + 1    
                        row_cell.append(self.binary_image[y:y+h, x:x+w])
        
                        # if(self.debug):
                        #     Utility.showImage(self.binary_image[y:y+h, x:x+w],"row cell (width,height) : ({0},{1})".format(w,h))
                    
                    i = i+1
                    
                    if(self.debug):
                        x_pos = int(x+5)
                        y_pos = int(y + h/2)
                        color = (0,255,0)
                        if(i%2 == 0):
                            color = (255,0,0)
                        
                        cv2.drawContours(self.paper, [cnt], 0, color, 3)
                        cv2.putText(self.paper, "{0}".format(i), (x_pos,y_pos),cv2.FONT_HERSHEY_SIMPLEX, 2, (2,255,0),2,cv2.LINE_AA)

        self.amountOfRow = amount_of_row
        student_id_cell = temp_cell[amount_of_row+1]
        if(self.debug):
            cnt = contour_sheet_sorted[4]
            Utility.showImage(self.paper,"image segment")
            Utility.showImage(student_id_cell,"student id cell (width,height) : ({0},{1})".format(w,h))


        return row_cell, student_id_cell





    