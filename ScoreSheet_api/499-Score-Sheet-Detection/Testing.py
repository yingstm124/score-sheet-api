import Utility
from Processing import *
import os

def getExpectResults(course):
    if(course == "201111"):
        return [
        {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [7.0, 8.0, 9.0, 6.0, 4.0,3.0,34]},
        {'studentID': '600510111', 'pageNo': [], 'fullScore': [], 'score': [4.0, 3.0, 2.0, 7.0, 8.0,10.0,34]},
        {'studentID': '600510112', 'pageNo': [], 'fullScore': [], 'score': [10.0, 10.0, 10.0, 10.0, 10.0,10.0,60]},
        {'studentID': '600510113', 'pageNo': [], 'fullScore': [], 'score': [6.0, 2.0, 1.0, 4.0, 8.0,9.0,55]},
        {'studentID': '600510114', 'pageNo': [], 'fullScore': [], 'score': [7.0, 7.0, 7.0, 6.0, 8.0,10.0,7]},
        {'studentID': '610510120', 'pageNo': [], 'fullScore': [], 'score': [7.0, 7.0, 8.0, 6.0, 2.0,3.0,43]},
        {'studentID': '610510121', 'pageNo': [], 'fullScore': [], 'score': [8.0, 8.0, 6.0, 7.0, 4.0,3.0,62]},
        {'studentID': '610510122', 'pageNo': [], 'fullScore': [], 'score': [2.0, 2.0, 3.0, 1.0, 4.0,9.0,79]},
        {'studentID': '610510123', 'pageNo': [], 'fullScore': [], 'score': [4.0, 4.0, 8.0, 9.0, 10.0,10.0,50]},
        {'studentID': '610510124', 'pageNo': [], 'fullScore': [], 'score': [7.0, 7.0, 6.0, 4.0, 7.0,10.0,19]}
        ]
    elif (course == "201211"):
        return [
        {'studentID': '590510137', 'pageNo': [], 'fullScore': [], 'score': [7.0, 6.0, 8.0, 7.0, 5.0,4.0,3.0,2.0,6.0,11.0,40.0]},
        {'studentID': '590510101', 'pageNo': [], 'fullScore': [], 'score': [10.0, 10.0, 10.0, 10.0, 10.0,10.0,10.0,4.0,10.0,14.0,100.0]},
        {'studentID': '590510102', 'pageNo': [], 'fullScore': [], 'score': [7.0, 8.0, 6.0, 9.0, 13.0,12.0,11.0,14.0,7.0,8.0,69.0]},
        {'studentID': '590510103', 'pageNo': [], 'fullScore': [], 'score': [4.0, 4.0, 8.0, 8.0, 7.0,4.0,2.0,3.0,10.0,15.0,55.0]},
        {'studentID': '590510104', 'pageNo': [], 'fullScore': [], 'score': [4.0, 7.0, 14.0, 18.0, 19.0,20.0,14.0,17.0,4.0,5.0,77.0]},
        {'studentID': '600510110', 'pageNo': [], 'fullScore': [], 'score': [7.0, 8.0, 6.0, 4.0, 3.0,2.0,1.0,0.0,4.0,33.0,27.0]},
        {'studentID': '600510111', 'pageNo': [], 'fullScore': [], 'score': [7.0, 7.0, 4.0, 3.0, 2.0,6.0,8.0,7.0,17.0,4.0,67.0]},
        {'studentID': '600510113', 'pageNo': [], 'fullScore': [], 'score': [3.0, 4.0, 8.0, 7.0, 6.0,5.0,4.0,2.0,10.0,14.0,76.0]},
        {'studentID': '610510120', 'pageNo': [], 'fullScore': [], 'score': [0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0]},
        {'studentID': '610510122', 'pageNo': [], 'fullScore': [], 'score': [3.0, 4.0, 7.0, 6.0, 6.0,7.0,19.0]}
        ]
    elif (course == "201251"):
        return [
            
        ]

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
root_path = os.path.dirname(__file__)
course_test_selected = "201211"
img_folders = "asset/inputs/{0}/".format(course_test_selected)
images = Utility.loadImages(os.path.join(root_path,img_folders))
expect_results = getExpectResults(course_test_selected)

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
    print("==> student id answer = {0}, result = {1}".format(expect_results[i]['studentID'],datas['studentID']))
    if(datas['studentID'] != 0):
        checkStudentID(expect_results[i]['studentID'],datas['studentID'])
    print("==> score")
    checkScores(expect_results[i]['score'],datas['score'])

# 3. report
