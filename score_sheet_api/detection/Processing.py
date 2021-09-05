import cv2
import numpy as np
import math
import score_sheet_api.detection.Utility as Utility
from keras.models import load_model
import os

class Sheets:

    def __init__(self, img, binaryImage, debug=False, max_cols=20):
        self.debug = debug
        self.original_image = img
        self.binary_image = binaryImage  
        self.min_width_cell =  self.binary_image.shape[1]/max_cols
        self.max_cols = max_cols  
        root_path = os.path.dirname(__file__)
        model_path = 'models/mnist.h5'
        self.model = load_model(os.path.join(root_path,model_path))

    def processing(self):
        ''' 
            - POC Issue sorted contours -

            [/] 1. get external cell by using external contouring
            [/] 2. get rows by using contouring
            [/] 3. order row and colum of cell
            [ ] 4. predict & mapping data structure 
                    : identify three part
                        - Text
                        - Number Text
                        - Handwritten (Model)
        '''
        datas = {
            "StudentId": str(),
            "pageNo":[],
            "fullScore": [],
            "Scores":[],
            "Message":"",
            "OldStudentId":str(),
            "OldScores":[]
        }
        contours, _ = Utility.contours(self.binary_image)
        binary_external_cell, rgb_external_cell = self.getExternalCell(contours,10)
        bi_rows, rgb_rows = self.boundingRows(binary_external_cell, rgb_external_cell,buffer=85)

        if(self.debug):
            Utility.showImage(self.binary_image, "orginal binary image")
            Utility.showImage(binary_external_cell, "number of row : {0}".format(len(bi_rows)))
            Utility.showImage(rgb_external_cell, "number of row : {0}".format(len(bi_rows)))

        # predict inside of row
        # loop rows
        for row in range(len(rgb_rows)):
        
            if(self.debug and len(rgb_rows[row]) > 0):
                Utility.showImage(rgb_rows[row], "show row {0}".format(row))
            binary_cols, rgb_cols = self.boundingCols(bi_rows[row],rgb_rows[row],15)
            # loop cols
            if(row == 0):
                is_student_cell = True
            else:
                is_student_cell = False
            
            for col in range(len(rgb_cols)):
                
                # segment digit and predict
                if(self.isDigitBox(row,col)):
                    digits = self.boundingDigits(binary_cols[col],rgb_cols[col], is_student_cell)
                    # loop digits in cell
                    result_digit = 0
                    for index, d in enumerate(digits):
                        digit_28_resized = Utility.resize28Image(d)
                        new_result_digit, accuracy = self.predict(digit_28_resized)
                        # predict digit
                        if(is_student_cell):
                            result_digit = int(str(result_digit) + str(new_result_digit))
                        else:
                            result_digit = result_digit + new_result_digit*math.pow(10,len(digits)-(index+1))
        
                        if(self.debug):
                            Utility.showImage(digit_28_resized,"28 x 28 digit size : {0} : {1}".format(result_digit, accuracy))
                    
                    if(is_student_cell):
                        datas["StudentId"] = result_digit
                    else:
                        datas["Scores"].append(int(result_digit))
 
                if(self.debug and len(rgb_cols[col]) > 0 and row not in [1,2]):
                    w = rgb_cols[col].shape[1]
                    h = rgb_cols[col].shape[0]
                    Utility.showImage(rgb_cols[col],"show row {0} col {1} : width x height = {2} x {3}".format(row,col,w,h))

        if(self.debug):
            print(datas)

        if(datas["StudentId"] == ""):
            datas["StudentId"] = 0

        return datas

    def isSquareBox(self, approx):
        return len(approx) == 4

    def isCellBox(self, approx, width):
        return len(approx) == 4 and (width > self.min_width_cell)

    def isDigitBox(self, row, col):
        # specific patern
        text_rows = [1,2] 
        return row not in text_rows and col > 0 

    def isDigit(self, width, height, min_width, min_height):
        return width > min_width and height > min_height

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

    def boundingRows(self, binary_img, rgb_img=None,buffer=0, debug=False):
        if(len(binary_img) < 1 and len(rgb_img) < 1):
            return [],[]
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        detect_horizontal = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        # segment row
        contours, _ = Utility.contours(detect_horizontal)
        contours, _ = Utility.sortContours(contours,method="top-to-bottom")
        
        if(rgb_img is not None):
            result = rgb_img.copy()
        else:
            result = None

        i = 0
        _, pre_y, _, _ = Utility.getAreaByContour(contours[0])
        bi_rows = []
        rgb_row = []
        for c in contours:
            x, y, _, _ = Utility.getAreaByContour(c)
            if(i > 0):
                if(i != 1):
                    start_pox_y = pre_y - buffer
                else:
                    start_pox_y = 0
                end_pos_y = y + buffer
                b_r = binary_img[start_pox_y:end_pos_y,:]
                rgb_r = rgb_img[start_pox_y:end_pos_y,:]
                if(debug):
                    Utility.showImage(rgb_r, "row {0}".format(i))
                bi_rows.append(b_r)
                rgb_row.append(rgb_r)

            if(debug and result is not None):
                cv2.putText(result, "{0}".format(i), (x,y),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),2,cv2.LINE_AA)
                cv2.drawContours(result, [c], -1, (36,255,12), 2)

            i += 1
            pre_y = y
        
        if(debug and result is not None):
            Utility.showImage(result, "result")
        
        return bi_rows, rgb_row

    def boundingCols(self, binary_img, rgb_img, buffer=0,debug=False):
        if(len(binary_img) < 1 and len(rgb_img) < 1):
            return [], []
        # segment col
        contours, _ = Utility.contours(binary_img, mode="RETR_TREE")
        contours, _ = Utility.sortContours(contours,method="left-to-right")
        max_width = binary_img.shape[1]
        i = 0
        bi_cols = []
        rgb_cols = [] 
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x, y, w, h = Utility.getAreaByContour(c)

            if(self.isSquareBox(approx) and w < max_width - 100 and w > 100):    
                rgb_col = rgb_img[y+buffer:y+h-buffer, x+buffer:x+w-buffer]
                bi_col = binary_img[y+buffer:y+h-buffer, x+buffer:x+w-buffer]
                bi_cols.append(bi_col)
                rgb_cols.append(rgb_col)
                
                if(debug): 
                    Utility.showImage(rgb_col, "col {0}".format(i))

                i += 1

        return bi_cols, rgb_cols

    def boundingDigits(self, binary_img, rgb_img, is_student_cell=False,debug=False):

        contours, _ = Utility.contours(binary_img)
        if(len(contours) == 0):
            return []
        contours, _ = Utility.sortContours(contours,method="left-to-right")

        cell_width = binary_img.shape[1]
        cell_height = binary_img.shape[0]
        if(is_student_cell):
            max_digit = 60
        else:
            max_digit = 3
 
        bi_digits = []
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x, y, w, h = Utility.getAreaByContour(c)
            min_width = 10
            min_height = cell_height/4
            digit = binary_img[y:y+h,x:x+w]

            if(self.isDigit(w,h,min_width,min_height)):
                bi_digits.append(digit)
                if(debug):
                    Utility.showImage(digit, "digit")


        return bi_digits

    def predict(self, img):
        img = img.reshape(1,28,28,1)
        img = img/255
        res = self.model.predict([img])[0]
        return np.argmax(res) , max(res)


    