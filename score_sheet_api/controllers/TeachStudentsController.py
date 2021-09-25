from score_sheet_api import app
from flask import Flask, request, jsonify, json
from score_sheet_api.config.database import getDb
from score_sheet_api.helpers.DbUtillity import Convert_to_Json, Handle_error

import pymysql

# initial database
cursor = getDb().cursor()


@app.route('/teachStudents', methods=['GET'])
def getTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'GET'):
        try: 
            query = '''SELECT TS.TeachStudentId, S.StudentId, S.FirstName, S.LastName, S.NickName, TS.SecNo 
                    From TeachStudents TS 
                    INNER JOIN Students S ON TS.StudentId = S.StudentId 
                    WHERE TS.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchall()
            
            if(res == None):
                print("No Content")
                return ('',204)
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)

    response = jsonify(res)
            
    return jsonify(res), 200


@app.route('/countTeachStudents', methods=['GET'])
def getCountTeachStudents():
    
    teach_course_id = request.args.get('teachCourseId')
    if(request.method == 'GET'):
        
        try: 
            query = '''Select COUNT(ts.TeachStudentId) AS Count FROM TeachCourses tc 
                    INNER JOIN TeachStudents ts ON tc.TeachCourseId = ts.TeachCourseId 
                    WHERE tc.TeachCourseId = {0}'''.format(teach_course_id)
            cursor.execute(query)
            res = cursor.fetchone()
            
            if(res == None):
                print("No Content")
                return ('',204)
        
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)
        
    return jsonify(res), 200

        

@app.route('/addTeachStudents', methods=['POST'])
def addTeachStudent():
    
    teach_course_id = request.args.get('teachCourseId') 
    if(request.method == 'POST'):
        '''
            => input body 
            {
                "StudentId": int
                "SecNo": int
            }
            => output body
            [
                {
                    "StudentId": int
                    "IsRegister": boolean
                    "SecNo":int
                }
            ]
        '''
        students = request.json
        
        
        try:
            insert_students = []
            for std in students:
                print(type(std))
                
                if(not isinstance(std,dict)):
                    std = json.loads(std)

                std_obj = {
                    "StudentId": std["StudentId"],
                    "IsRegister": False,
                    "SecNo": int(std["SecNo"])
                }

                # check student in system ?
                query_find = '''
                    SELECT StudentId 
                    FROM Students 
                    WHERE StudentId = {0}'''.format(int(std["StudentId"]))
                cursor.execute(query_find)
                res = cursor.fetchone()
                    
                if(res != None):
                    # check student duplicate on teach student ?
                    query_find = ''' 
                        SELECT T.TeachStudentId
                        FROM TeachStudents T
                        WHERE T.StudentId = {0} AND T.TeachCourseId = {1}
                    '''.format(std["StudentId"], teach_course_id)
                    cursor.execute(query_find)
                    teachStudent = cursor.fetchone()

                    if(teachStudent == None): 
                        std_obj["IsRegister"] = True
                
                insert_students.append(std_obj)
                
            # loop for insert
            for insert_student in insert_students:

                if(insert_student["IsRegister"]):
                    query = '''
                                INSERT INTO TeachStudents(StudentId, TeachCourseId, SecNo) 
                                VALUES(%s,%s,%s)'''
                    cursor.execute(query,(int(insert_student["StudentId"]), int(teach_course_id), int(insert_student["SecNo"])))
                    teachStudentId = cursor.lastrowid
                    getDb().commit()

                    # check assignment from teach course id
                    query = ''' 
                                SELECT AssignmentId 
                                FROM Assignments
                                WHERE TeachCourseId = {0}'''.format(teach_course_id)
                    cursor.execute(query)
                    assignmentIds = cursor.fetchall()

                    if(assignmentIds != None):
                        for assignmentId in assignmentIds:
                            q = '''
                                    INSERT INTO StudentAssignments (TeachStudentId,AssignmentId) 
                                    VALUES(%s,%s)'''
                            cursor.execute(q, (int(teachStudentId),int(assignmentId["AssignmentId"])))
                            getDb().commit()


            response = jsonify(insert_students)
            return jsonify(insert_students), 200

        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  


@app.route('/deleteTeachStudent', methods=['POST'])
def deleteTeachStudent():
    
    teachStudentId = request.args.get('teachStudentId')
    if(request.method == 'POST'):
        
        try:
            
            query = '''Delete From StudentAssignments 
                    Where TeachStudentId = {0}'''.format(int(teachStudentId))
            cursor.execute(query)
            getDb().commit()
            
            query = '''Delete From TeachStudents 
                    Where TeachStudentId = {0}'''.format(int(teachStudentId))
            cursor.execute(query)
            getDb().commit()
            
            return jsonify(True), 200
        
        except pymysql.Error as err:
            print(err)
            return Handle_error(err, 500)  
        
    return jsonify(False), 200