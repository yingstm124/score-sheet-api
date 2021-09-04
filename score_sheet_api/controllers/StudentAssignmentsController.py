import re
from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import pymysql

# initial database
cursor = getDb().cursor()

@app.route('/studentAssignments',methods=['GET'])
def getStudentAssignments():
    
    teach_course_id = request.args.get('teachCourseId')
    if(request.method == 'GET'):
        try: 
            query = "SELECT SA.StudentAssignmentId, SA.TeachStudentId, SA.Img, TS.StudentId, TS.SecNo,S.FirstName, S.LastName FROM StudentAssignments SA INNER JOIN TeachStudents TS ON SA.TeachStudentId = TS.TeachStudentId INNER JOIN Students S ON S.StudentId = TS.StudentId Where TS.TeachCourseId = {0};".format(int(teach_course_id))
            cursor.execute(query)
            res = cursor.fetchall()
            
            if(res == None):
                print("No content")
                return ('',204)
            
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
    
    return jsonify(res), 200

'''
    Save Student Score & Score Record Api
        Case 1: Found Student
            Case 1.1 : never detect, insert Score Records
            Case 1.2 : already detect, update Score Records
        Case 2: Not Found Student
            - No save 
'''
@app.route('/saveScoreRecord',methods=['POST'])
def saveScoreRecord():

    '''
        request = {
            "Scores": list
            "StudentId": int
            "AssignmentId": int
            "TeachCourseId": int
        }
    '''
    request_scores = request.json

    response = {
        "Message": str()
    }

    if(request.method == "POST"):
        try:
            # check Student ID
            query = "select S.StudentId from students S inner join teachStudents TS on TS.StudentId = S.StudentId Where S.StudentId = {0} And TS.TeachCourseId = {1}".format(student_id,teachcourse_id)
            cursor.execute(query)
            res = cursor.fetchone()

            # Case 2 : No save
            if(res == None):
                response["Message"] = "Not Found Student"
                return ('',204)
            
            # Case 1 : Found Student
            else:
                query = "select SS.Score from studentscores SS inner join scores S on SS.ScoreId = S.ScoreId inner join assignments A on S.AssignmentId = A.AssignmentId Where S.AssignmentId = {0} And  A.AssignmentId = {1}".format(found_student_id,assignment_id)
                cursor.execute(query)
                res = cursor.fetchall()

                # Case 1.1 : never detect, insert Score Records
                if(res == None):
                    for score in request_scores["Scores"]:
                        query_insert_score = "INSERT INTO Scores(AssignmentId) VALUES(%s,%s)"
                        res = cursor.execute(query_insert_score,(request_scores["AssignmentId"],score))
                        score_id = res.lastrowid
                        getDb().commit()

                        query_insert_student_score = "INSERT INTO StudentScores(ScoreId,Score) VALUES(%s,%s)"
                        res = cursor.execute(query_insert_student_score,(score_id,score))
                        getDb().commit()

                    return jsonify(True), 200

                # Case 1.2 : already detect, update Score Records
                else:
                    # Not yet !!
                    return jsonify(True), 200

        except pymysql.Error as err:
            return Handle_error(err,500)



