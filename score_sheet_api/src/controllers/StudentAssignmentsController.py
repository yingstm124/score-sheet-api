from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error

import pymysql
import decimal


# initial database
cursor = getDb().cursor()

@app.route('/studentAssignments',methods=['GET'])
def getStudentAssignments():
    
    assignment_id = request.args.get('AssignmentId')
    if(request.method == 'GET'):
        try: 
            query = '''
                SELECT SA.StudentAssignmentId, SA.TeachStudentId, SA.Img, TS.StudentId, TS.SecNo,S.FirstName, S.LastName, SA.Score 
                FROM StudentAssignments SA 
                INNER JOIN TeachStudents TS ON SA.TeachStudentId = TS.TeachStudentId 
                INNER JOIN Students S ON S.StudentId = TS.StudentId 
                Where SA.AssignmentId = {0} '''.format(int(assignment_id))
            cursor.execute(query)
            res = cursor.fetchall()
            headers = [x[0] for x in cursor.description]
            for r in res:
                if(r.Score != None ):
                    r.Score = int(r.Score)
                else:
                    r.Score = 0
            
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
    
    return Convert_to_Json(headers, res)