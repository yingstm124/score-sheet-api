from Processing import *
import Utility
import cv2

if __name__ == '__main__':
    
    # 1. import original rgb image 
    #img = cv2.imread('/Users/macbook/Desktop/204499_independence/Code/ScoreSheet_api/499-Score-Sheet-Detection/asset/sample01.png')
    img = cv2.imread(r"C:\Users\yings\Desktop\204491_Independence\499-score-sheet-app\ScoreSheet_api\499-Score-Sheet-Detection\asset\sample01.png")

    # 2. convert to binary image
    gray_img = Utility.convertBgr2GrayImage(img)
    img = Utility.removeNoiseAndShadow(gray_img)
    binary_img = Utility.convertGray2BinaryImage(img)

    # 3. image processing & segmentation & prediction  
    datas = Sheets(img, binary_img, True).processing()
