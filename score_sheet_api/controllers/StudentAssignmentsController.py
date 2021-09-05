from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import pymysql
import decimal


# initial database
cursor = getDb().cursor()

@app.route('/studentAssignments',methods=['GET'])
def getStudentAssignments():
    
    assignment_id = request.args.get('AssignmentId')
    if(request.method == 'GET'):
        try: 
            query = "SELECT SA.StudentAssignmentId, SA.TeachStudentId, SA.Img, TS.StudentId, TS.SecNo,S.FirstName, S.LastName, SA.Score FROM StudentAssignments SA INNER JOIN TeachStudents TS ON SA.TeachStudentId = TS.TeachStudentId INNER JOIN Students S ON S.StudentId = TS.StudentId Where SA.AssignmentId = {0} group by TS.StudentId;".format(int(assignment_id))
            cursor.execute(query)
            res = cursor.fetchall()
            for r in res:
                print(r['Score'])
                if(r['Score'] != None ):
                    r['Score'] = int(r['Score'])
                else:
                    r['Score'] = 0

            if(res == None):
                print("No content")
                return ('',204)
            
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
    
    return jsonify(res), 200