from ImageProcessing import *
from Segmentation import *
from Prediction import *


import cv2




if __name__ == '__main__':
    
    # 1. import original rgb image 
    img = cv2.imread('/Users/macbook/Desktop/204499_independence/Code/ScoreSheet_api/499-Score-Sheet-Detection/asset/sample01.png')
    #Utility.showImage(img, 'original image')

    # 2. convert to binary image
    binary_image = BinaryImage(img, True).getBinaryImage()

    # 3. processing cell
    row_cell, student_id_cell = CellSheets(binary_image, True).getCellSheets()


    # cellBoxs = cell_sheets.scoreSheet
    # amount_of_row = cell_sheets.amountOfRow
    # print("amount of row : ",amount_of_row)
    # print(cellBoxs) 
    
    

    