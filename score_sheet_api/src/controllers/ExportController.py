from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error

import os
import pymysql
import werkzeug

# initial database
cursor = getDb().cursor()

@app.route('/exportScoreInfo', methods=['GET'])
def getExportInfo():

    teach_course_id = request.args.get('teachCourseId')
    if(request.method == "GET"):

        try:
            query = '''
                    SELECT S.StudentId, CONCAT(S.FirstName , ' ' ,Lastname) AS FullName, A.AssignmentName, SA.Score, A.FullScore
                    FROM TeachStudents TS
                    INNER JOIN Students S ON TS.StudentId = S.StudentId
                    INNER JOIN StudentAssignments SA ON SA.TeachStudentId = TS.TeachStudentId
                    INNER JOIN Assignments A ON SA.AssignmentId = A.AssignmentId
                    WHERE TS.TeachCourseId = {0}
            '''.format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchall()
            headers = [x[0] for x in cursor.description]

            if(res == None):
                return ('',204)
        

        except Exception as err:
            print(err)
            return Handle_error(err,500)

        return Convert_to_Json(headers, res)