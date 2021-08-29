from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

# prediction
import score_sheet_api.detection.Processing as Processing
import score_sheet_api.detection.Utility as Utility

import os
import pymysql
import cv2
import werkzeug


# initial database
cursor = getDb().cursor()

@app.route('/predict', methods=['POST'])
def predict():

    if(request.method == "POST"):

        try:
            if(request.files['image']):
                # 1. predict image
                image = request.files['image']
                filename = werkzeug.utils.secure_filename(image.filename)
                pathImage = os.path.join(app.root_path,'./static/predicts',filename)
                image.save(pathImage)

                image = cv2.imread(pathImage)
                gray_image = Utility.convertBgr2GrayImage(image)
                binary_image = Utility.convertGray2BinaryImage(gray_image)
     
                datas = Processing.Sheets(image, binary_image, True).processing()
                print(datas)
                # 2. fetch data for validation 
                # 2.1 validate student id of assignment  
        except Exception as err:
            print(err)
            return Handle_error(False)
