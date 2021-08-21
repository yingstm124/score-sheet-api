import Utility
from Processing import *
import os

root_path = os.path.dirname(__file__)
img_folders = "asset/inputs/"

def report(answer, result):
    if(answer == result):
        print("[/] Correct! answer = {0} , result = {1} ".format(answer, result))
    else:
        print("[X] Incorrect! answer = {0} , result = {1} ".format(answer, result))

def checkStudentID(ans_std, std):
    for i in range(len(ans_std)):
        if(i < len(str(std))):
            report(ans_std[i], str(std)[i])

def checkScores(ans_scores, scores):
    for i in range(len(ans_scores)):
        if(i < len(scores)):
            report(ans_scores[i], scores[i])

# 1. load images in floder
images = Utility.loadImages(os.path.join(root_path,img_folders))
expect_results = [
    {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [5.0, 10.0, 6.0, 7.0, 8.0,4.0,85.0]},
    {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [4.0, 4.0, 8.0, 10.0, 9.0, 6.0,2.0,0.0,7.0,6.0,66]},
    {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [7.0, 8.0, 4.0, 3.0, 2.0,6.0,27.0]},
    {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [5.0, 7.0, 8.0, 19.0]}
]

# 2. run result
for i in range(len(images)):
    img = images[i]
    # 2.1 convert to binary image
    gray_img = Utility.convertBgr2GrayImage(img)
    img = Utility.removeNoiseAndShadow(gray_img)
    binary_img = Utility.convertGray2BinaryImage(img)

    # 2.2 test image processing & segmentation & prediction  
    print('----------------test image {0}------------------'.format(i+1))
    datas = Sheets(img, binary_img).processing()
    print("==> student id")
    checkStudentID(expect_results[i]['studentID'],datas['studentID'])
    print("==> score")
    checkScores(expect_results[i]['score'],datas['score'])

# 3. report
