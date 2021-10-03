from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error

# prediction
import score_sheet_api.src.detection.Processing as Processing
import score_sheet_api.src.detection.Utility as Utility

import os
import pymysql
import cv2
import werkzeug


# initial database
cursor = getDb().cursor()

@app.route('/predict', methods=['POST'])
def predict():
    
    teachCourse_id = request.args.get('teachCourseId')
    assignment_id = request.args.get('assignmentId')
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

                '''
                    datas = {
                        "StudentId": int
                        "pageNo": list
                        "fullScore": list
                        "Scores": list
                        "Message": string,
                        "OldStudentId": int,
                        "OldScores": list,
                        "TeachStudentId":int
                    }
                '''
                datas = Processing.Sheets(image, binary_image).processing()
                result_studentId = datas["StudentId"]
                result_scores = datas['Scores']
                os.remove(pathImage)

                # check Student ID
                query = '''
                    select S.StudentId, TS.TeachStudentId 
                    from students S 
                    inner join teachStudents TS on TS.StudentId = S.StudentId 
                    Where S.StudentId = {0} And TS.TeachCourseId = {1}'''.format(result_studentId,teachCourse_id)
                cursor.execute(query)
                res = cursor.fetchone()

                if(res != None):
                    datas["Message"] = "Found Student"
                    datas["TeachStudentId"] = res.TeachStudentId
                    found_student_id = res.StudentId
                    query = '''
                        select SS.Score 
                        from studentscores SS 
                        inner join scores S on SS.ScoreId = S.ScoreId 
                        inner join assignments A on S.AssignmentId = A.AssignmentId 
                        Where S.AssignmentId = {0} And  A.AssignmentId = {1}'''.format(found_student_id,assignment_id)
                    cursor.execute(query)
                    res = cursor.fetchall()
                    if(len(res) == 0):
                         return datas

                    old_scores = []
                    for r in res:
                        old_scores.append(r.FullScore)
                    datas["OldScore"] = old_scores
                    return datas

                else:
                    datas["Message"] = "Not Found Student"
                    return datas

                return datas
                
        except Exception as err:
            print(err)
            return Handle_error(False)
