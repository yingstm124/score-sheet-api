from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import werkzeug
import pymysql

# initial database
cursor = getDb().cursor()


'''
    Save Student Score & Score Record Api
        Case 1: Found Student
            Case 1.1 : never detect, insert Score Records
            Case 1.2 : already detect, update Score Records
        Case 2: Not Found Student
            - No save 
'''
@app.route('/saveScore',methods=['POST'])
def saveScore():

    '''
        request = {
            "Scores": list
            "StudentId": int
            "AssignmentId": int
            "TeachCourseId": int
        }
    '''
    # scores = request.args.get('Scores')
    # student_id = request.args.get('StudentId')
    # assignment_id = request.args.get('AssignmentId')
    # teachcourse_id = request.args.get('TeachCourseId')

    scores = request.json["Scores"]
    student_id = request.json["StudentId"]
    teach_student_id = request.json["TeachStudentId"]
    assignment_id = request.json['AssignmentId']
    teachcourse_id = request.json["TeachCourseId"]

    response = {
        "Message": str()
    }

    if(request.method == "POST"):
        try:
            # check Student ID
            query = '''select S.StudentId 
                        from students S 
                        inner join teachStudents TS on TS.StudentId = S.StudentId 
                        Where S.StudentId = {0} And TS.TeachCourseId = {1} '''.format(student_id,teachcourse_id)
            cursor.execute(query)
            res = cursor.fetchone()

            # Case 2 : No save
            if(res == None):
                response["Message"] = "Not Found Student"
                return Handle_error(err,500)
            
            # Case 1 : Found Student
            else:
                query = '''select SS.StudentScoreId, SS.StudentId, S.ScoreId
                            from studentscores SS
                            inner join scores S on S.ScoreId = SS.ScoreId 
                            Where SS.StudentId = {0} And  SS.AssignmentId = {1}'''.format(student_id,assignment_id)

                cursor.execute(query)
                res = cursor.fetchall()

                # Case 1.1 : never detect, insert Score Records
                if(len(res) == 0):
                    for index, score in enumerate(scores):
                        query_insert_score = '''INSERT INTO Scores(AssignmentId,score, pageNo) 
                                                VALUES(%s,%s,%s)'''
                        cursor.execute(query_insert_score,(assignment_id, score, index+1))
                        score_id = cursor.lastrowid
                        getDb().commit()

                        query_insert_student_score = '''INSERT INTO StudentScores(StudentId,ScoreId,Score,AssignmentId) 
                                                        VALUES(%s,%s,%s,%s)'''
                        res = cursor.execute(query_insert_student_score,(int(student_id),int(score_id),int(score),int(assignment_id)))
                        getDb().commit()

                    return jsonify(response), 200

                # Case 1.2 : already detect, update Score Records
                else:
                    # update student score by student score Id
                    for index, score in enumerate(scores):
                        if(index < len(scores)):
                            query = ''' update Scores 
                                    SET Score=%s,PageNo=%s
                                    WHERE ScoreId = {0} '''.format(int(res[index]["ScoreId"]))
                            cursor.execute(query, (int(score),int(index+1)))
                            getDb().commit()

                # Find Student Assignment Id
                query_select_id = '''select SA.StudentAssignmentId 
                                    from studentassignments SA 
                                    Where TeachStudentId = {0} AND AssignmentId = {1}'''.format(teach_student_id,assignment_id)
                cursor.execute(query_select_id)
                res = cursor.fetchone()
                student_assign_id = res["StudentAssignmentId"]

                query_update = '''UPDATE StudentAssignments 
                                SET Score=%s 
                                Where StudentAssignmentId=%s'''
                cursor.execute(query_update,(sum(scores),int(student_assign_id)))
                getDb().commit()

                response["Message"] = "Already Detect"
                return jsonify(response), 200

        except pymysql.Error as err:
            return Handle_error(err,500)




