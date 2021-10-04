from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.src.config.database import getDb
from score_sheet_api.src.helpers.DbUtillity import Convert_to_Json, Handle_error, Covert_to_Object_Json

import pymysql

# initial database
cursor = getDb().cursor()

@app.route('/assignments', methods=['GET'])
def getAssignments():
    
    teach_course_id = request.args.get('teachCourseId') 
    if (request.method == 'GET'):
        
        try: 
            query = '''
                        SELECT * 
                        From Assignments A 
                        WHERE A.TeachCourseId = ?'''
            cursor.execute(query, teach_course_id)
            res = cursor.fetchall()
            headers = [x[0] for x in cursor.description]
            
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
        
    return Convert_to_Json(headers, res)



@app.route('/countAssignments', methods=['Get'])
def getCountAssignments():
    
    teach_course_id = request.args.get('teachCourseId')
    if(request.method == 'GET'):
        
        try:
            query = '''
                SELECT COUNT(A.AssignmentId) as Count 
                From Assignments A 
                WHERE A.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)

            res = {'Count': cursor.fetchone().Count}
            
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)

        return jsonify(res)
    
    
@app.route('/addAssignment',methods=['POST'])
def addAssignment():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'POST'):

        '''
        input {
            'AssignmentName': 
            'FullScore':
        }
        '''

        assignmentName = request.json['AssignmentName']
        fullScore = request.json['FullScore']
        
        try:
            # check teach students
            query_select_teachstd = '''
                                        SELECT TeachStudentId 
                                        FROM TeachStudents 
                                        WHERE TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query_select_teachstd)
            teach_stds = cursor.fetchall()

            #insert assignment
            query_insert = ''' 
                            INSERT INTO Assignments (TeachCourseId,FullScore,AssignmentName)
                            VALUES(?,?,?)'''
            cursor.execute(query_insert,(teach_course_id, fullScore, assignmentName))
            cursor.commit()

            cursor.execute("SELECT @@IDENTITY AS ID")
            assignment_id = cursor.fetchone().ID     

            if(len(teach_stds) != 0):
                for teach_std in teach_stds:
                    query_add = '''
                            INSERT INTO StudentAssignments (TeachStudentId, AssignmentId) 
                            VALUES (?,?)'''
                    cursor.execute(query_add,(int(teach_std.TeachStudentId),int(assignment_id)))
                    cursor.commit()
            
            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err.args[0],err.args[1])
            return Handle_error(err, 500)  


@app.route('/deleteAssignment', methods=['POST'])
def deleteAssignment():
    
    AssignmentId = request.args.get('AssignmentId')
    if(request.method == 'POST'):
        
        try:
            query = "Delete From StudentScores Where AssignmentId = ?;"
            cursor.execute(query, int(AssignmentId))
            cursor.commit()

            query = "Delete From StudentAssignments Where AssignmentId = ?;"
            cursor.execute(query, int(AssignmentId))
            cursor.commit()

            query = "Delete From Assignments Where AssignmentId = ?;"
            cursor.execute(query, int(AssignmentId))
            cursor.commit()

            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  
        
    return jsonify(False), 200

@app.route('/editAssignment', methods=['POST'])
def editAssignment():

    AssignmentId = request.args.get('AssignmentId')
    AssignmentName = request.json['AssignmentName']
    if(request.method == 'POST'):
        try:
            query = '''
                    UPDATE Assignments
                    SET AssignmentName=?
                    WHERE AssignmentId=?
            '''
            cursor.execute(query,(AssignmentName, AssignmentId))
            cursor.commit()

            return jsonify(True), 200

        except pymysql.Error as err:
            return Handle_error(err, 500)
